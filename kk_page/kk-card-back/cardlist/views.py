import os
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Card, RecommendResult
from .serializers import CardSerializer, ResultSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend

from .filters import CardFilter
from .models import RecommendResult
from django.shortcuts import get_object_or_404

from .ai_recommend import (
    analyze_answers,
    get_persona,
    get_candidate_cards,
    make_candidate_payload,
    call_gemini_recommendation,
)

@api_view(["GET"])
def card_list(request):
    cards = Card.objects.all()
    card_filter = CardFilter(
        request.query_params,
        queryset=cards,
    )
    if not card_filter.is_valid():
        return Response(
            card_filter.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    serializer = CardSerializer(card_filter.qs, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def card_detail(request, card_pk):
    try:
        card = Card.objects.get(pk=card_pk)
    except Card.DoesNotExist:
        return Response({"message": "카드를 찾을 수 없습니다."}, status=404)

    serializer = CardSerializer(card)
    return Response(serializer.data)


@api_view(["GET"])
def recommend_cards(request):
    category = request.GET.get("category", "")
    limit = int(request.GET.get("limit", 3))

    cards = Card.objects.all()
    scored_cards = []

    for card in cards:
        score = 0
        benefits = card.benefits or {}

        if category in benefits:
            score += len(benefits[category]) * 10

        if "기타" in benefits:
            score += len(benefits["기타"])

        scored_cards.append((card, score))

    scored_cards.sort(key=lambda x: x[1], reverse=True)

    recommended_cards = [card for card, score in scored_cards[:limit]]
    serializer = CardSerializer(recommended_cards, many=True)

    return Response(serializer.data)

@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def recommend_results(request):
    # 내 저장 결과 조회
    if request.method == "GET":
        results = (
            RecommendResult.objects
            .filter(user=request.user)
            .prefetch_related("card_list")
            .order_by("-id")
        )

        serializer = ResultSerializer(
            results,
            many=True,
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # 추천 결과 저장
    serializer = ResultSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    persona_title = serializer.validated_data["persona_title"]
    persona_description = serializer.validated_data.get(
        "persona_description",
        "",
    )

    selected_cards = serializer.validated_data["card_list"]
    selected_card_ids = sorted(
        card.id for card in selected_cards
    )

    # 같은 사용자의 동일 페르소나 결과 확인
    existing_results = (
        RecommendResult.objects
        .filter(
            user=request.user,
            persona_title=persona_title,
            persona_description=persona_description,
        )
        .prefetch_related("card_list")
    )

    # 추천 카드 3개까지 동일하면 중복으로 판단
    for existing_result in existing_results:
        existing_card_ids = sorted(
            card.id
            for card in existing_result.card_list.all()
        )

        if existing_card_ids == selected_card_ids:
            return Response(
                {
                    "detail": "이미 저장된 추천 결과입니다.",
                    "already_saved": True,
                    "result_id": existing_result.id,
                },
                status=status.HTTP_200_OK,
            )

    # 동일한 결과가 없을 때만 새로 저장
    result = serializer.save(user=request.user)

    response_serializer = ResultSerializer(result)

    return Response(
        {
            "detail": "추천 결과가 저장되었습니다.",
            "already_saved": False,
            "result": response_serializer.data,
        },
        status=status.HTTP_201_CREATED,
    )

# @api_view(["GET", "POST"])
# @permission_classes([IsAuthenticated])
# def recommend_results(request):
#     # 내 저장 결과 조회
#     if request.method == "GET":
#         results = (
#             RecommendResult.objects
#             .filter(user=request.user)
#             .prefetch_related("card_list")
#             .order_by("-id")
#         )

#         serializer = ResultSerializer(
#             results,
#             many=True,
#         )

#         return Response(
#             serializer.data,
#             status=status.HTTP_200_OK,
#         )

#     # 추천 결과 저장
#     serializer = ResultSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     persona_title = serializer.validated_data["persona_title"]
#     persona_description = serializer.validated_data.get(
#         "persona_description",
#         "",
#     )

#     selected_cards = serializer.validated_data["card_list"]
#     selected_card_ids = sorted(
#         card.id for card in selected_cards
#     )

#     # 같은 사용자의 동일 페르소나 결과 확인
#     existing_results = (
#         RecommendResult.objects
#         .filter(
#             user=request.user,
#             persona_title=persona_title,
#             persona_description=persona_description,
#         )
#         .prefetch_related("card_list")
#     )

#     # 추천 카드 3개까지 동일하면 중복으로 판단
#     for existing_result in existing_results:
#         existing_card_ids = sorted(
#             card.id
#             for card in existing_result.card_list.all()
#         )

#         if existing_card_ids == selected_card_ids:
#             return Response(
#                 {
#                     "detail": "이미 저장된 추천 결과입니다.",
#                     "already_saved": True,
#                     "result_id": existing_result.id,
#                 },
#                 status=status.HTTP_200_OK,
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST,
#         )
    


@api_view(['POST'])
def ai_recommend_cards(request):
    answers = request.data.get('answers', [])

    if not answers:
        return Response(
            {'detail': '설문 답변이 없습니다.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    analysis = analyze_answers(answers)

    card_type = analysis['card_type']
    selected_category = analysis['selected_category']
    category_score = analysis['category_score']

    # 페르소나는 카드 타입과 무관하게 카테고리로만 결정
    persona = get_persona(selected_category)

    # 추천 후보는 카드 타입으로 필터링
    candidate_cards = get_candidate_cards(
        Card=Card,
        card_type=card_type,
        selected_category=selected_category,
        category_score=category_score,
        limit=30,
    )


    if not candidate_cards:
        return Response(
            {'detail': '추천 후보 카드가 없습니다.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    candidate_payload = make_candidate_payload(
        candidate_cards=candidate_cards,
        selected_category=selected_category,
    )

    ai_used = False
    ai_provider = 'fallback'

    try:
        use_gemini = getattr(settings, "USE_GEMINI", False)
        gemini_api_key = getattr(settings, "GEMINI_API_KEY", None)

        print("====== Gemini 설정 확인 ======")
        print("USE_GEMINI:", use_gemini)
        print("GEMINI_API_KEY 있음?:", bool(gemini_api_key))
        print("GEMINI_MODEL:", getattr(settings, "GEMINI_MODEL", None))

        if use_gemini and gemini_api_key:
            ai_data = call_gemini_recommendation(
                answers=answers,
                card_type=card_type,
                selected_category=selected_category,
                category_score=category_score,
                persona=persona,
                candidate_payload=candidate_payload,
            )
            ai_used = True
            ai_provider = 'gemini'
        else:
            ai_data = {
                'recommended_card_ids': [card.id for card in candidate_cards[:3]],
                'type_reason': '설문 응답에서 가장 높은 점수를 받은 소비 카테고리를 기준으로 소비 유형을 분석했습니다.',
                'common_benefits': '추천 카드들은 선택된 소비 카테고리와 관련된 혜택을 중심으로 구성되어 있습니다.',
                'recommend_reason': '사용자의 주요 소비 성향과 카드 혜택이 잘 맞는 후보 카드를 우선 추천했습니다.',
                'card_reasons': [],
            }

    except Exception as error:
        print('Gemini 추천 오류:', error)

        ai_data = {
            'recommended_card_ids': [card.id for card in candidate_cards[:3]],
            'type_reason': 'AI 추천 중 오류가 발생하여 설문 점수 기반으로 추천했습니다.',
            'common_benefits': '추천 카드들은 선택된 소비 카테고리와 관련된 혜택을 중심으로 구성되어 있습니다.',
            'recommend_reason': '사용자의 소비 성향과 카드 혜택이 직접적으로 연결되는 후보 카드를 우선 추천했습니다.',
            'card_reasons': [],
        }

    recommended_ids = ai_data.get('recommended_card_ids', [])

    valid_candidate_ids = [card.id for card in candidate_cards]

    valid_recommended_ids = [
        card_id for card_id in recommended_ids
        if card_id in valid_candidate_ids
    ]

    if len(valid_recommended_ids) < 3:
        for card in candidate_cards:
            if card.id not in valid_recommended_ids:
                valid_recommended_ids.append(card.id)

            if len(valid_recommended_ids) == 3:
                break

    final_ids = valid_recommended_ids[:3]

    final_cards = Card.objects.filter(id__in=final_ids)

    final_cards = sorted(
        final_cards,
        key=lambda card: final_ids.index(card.id),
    )

    serializer = CardSerializer(final_cards, many=True)

    return Response({
        'cards': serializer.data,
        'persona': persona,
        'selected_category': selected_category,
        'category_score': category_score,
        'ai_summary': {
            'type_reason': ai_data.get('type_reason', ''),
            'common_benefits': ai_data.get('common_benefits', ''),
            'recommend_reason': ai_data.get('recommend_reason', ''),
            'card_reasons': ai_data.get('card_reasons', []),
        },
        'ai_used': ai_used,
        'ai_provider': ai_provider,
    })

    # 동일한 결과가 없을 때만 새로 저장
    # result = serializer.save(user=request.user)

    # response_serializer = ResultSerializer(result)

    # return Response(
    #     response_serializer.data,
    #     status=status.HTTP_201_CREATED,
    # )

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def recommend_result_detail(request, result_pk):
    result = get_object_or_404(
        RecommendResult,
        id=result_pk,
        user=request.user,
    )
    result.delete()
    return Response(
        status=status.HTTP_204_NO_CONTENT,
    )
