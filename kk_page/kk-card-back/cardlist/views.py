from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from .models import Card, RecommendResult
from .serializers import CardSerializer, ResultSerializer
from rest_framework.permissions import IsAuthenticated

from .filters import CardFilter

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

@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def recommend_results(request):
    if request.method =="GET":
        results = (
            RecommendResult.objects
            .filter(user=request.user)
            .prefetch_related("card_list")
            .order_by("-id")
        )
        serializer = ResultSerializer(
            results,
            many=True
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
    if request.method == "POST":
        serializer = ResultSerializer(
            data=request.data,
        )
        if serializer.is_valid():
            result = serializer.save(
                user=request.user,
            )
            Response_serizlier = ResultSerializer(
                result,
            )
            return Response(
                Response_serizlier.data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )