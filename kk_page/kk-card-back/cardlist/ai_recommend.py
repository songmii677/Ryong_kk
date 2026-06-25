import json
import os

from django.conf import settings
from google import genai


def normalize_benefits(benefits):
    if benefits is None:
        return {}

    if isinstance(benefits, dict):
        return benefits

    if isinstance(benefits, str):
        try:
            return json.loads(benefits)
        except json.JSONDecodeError:
            return {}

    return {}


def analyze_answers(answers):
    category_score = {}
    card_type = 'credit'

    for answer in answers:
        key = answer.get('key')
        value = answer.get('value')

        if key == 'card_type':
            card_type = value

        if key == 'category':
            category_score[value] = category_score.get(value, 0) + 1

    selected_category = None

    if category_score:
        selected_category = sorted(
            category_score.items(),
            key=lambda item: item[1],
            reverse=True
        )[0][0]

    return {
        'card_type': card_type,
        'selected_category': selected_category,
        'category_score': category_score,
    }


def get_persona(category):
    if category == '음식/카페':
        return {
            'title': '☕ 미식 탐험가',
            'desc': '맛있는 한 끼로 하루를 충전하는 타입',
        }

    if category == '통신':
        return {
            'title': '📱 통신비 지킴이',
            'desc': '매달 빠져나가는 비용도 꼼꼼하게 챙기는 타입',
        }

    if category == '쇼핑/간편결제':
        return {
            'title': '🛍️ 스마트 쇼퍼',
            'desc': '마음에 드는 걸 발견하면 그냥 지나치지 못하는 타입',
        }
    
    if category == '주유/교통':
        return {
            'title': '🚕 프로 이동러',
            'desc': '시간과 이동 비용까지 효율적으로 챙기는 타입',
        }
    
    if category == '교육/건강':
        return {
            'title': '✨ 성장형 인간',
            'desc': '조금씩 더 나은 나를 만들어가는 타입',
        }

    if category == '여행':
        return {
            'title': '✈️ 경험 수집가',
            'desc': '새로운 장소와 특별한 순간을 즐기는 타입',
        }

    if category == '문화/생활':
        return {
            'title': '🎧 취미 수집가',
            'desc': '소소한 즐거움으로 일상을 채우는 타입',
        }

    if category == '기타':
        return {
            'title': '✨ 어디서나 알뜰룡',
            'desc': '특정 장소보다 전체 결제에서 꾸준히 혜택을 챙기는 타입',
        }

    return {
        'title': '🌱 사회초년생',
        'desc': '다양한 관심사와 소비 패턴을 가진 타입',
    }


def get_candidate_cards(Card, card_type, selected_category, category_score, limit=30):
    queryset = Card.objects.filter(card_type=card_type)

    scored_cards = []

    for card in queryset:
        benefits = normalize_benefits(getattr(card, 'benefits', {}))

        score = 0

        for category, count in category_score.items():
            category_benefits = benefits.get(category, [])

            if category_benefits:
                score += count * 3
                score += min(len(category_benefits), 5)

        if selected_category and benefits.get(selected_category):
            score += 5

        if score > 0:
            scored_cards.append((score, card))

    scored_cards.sort(key=lambda item: item[0], reverse=True)

    candidate_cards = [card for score, card in scored_cards[:limit]]

    if not candidate_cards:
        candidate_cards = list(queryset[:limit])

    return candidate_cards


def make_candidate_payload(candidate_cards, selected_category):
    candidate_payload = []

    for card in candidate_cards:
        benefits = normalize_benefits(getattr(card, 'benefits', {}))

        candidate_payload.append({
            'id': card.id,
            'name': getattr(card, 'name', ''),
            'company': getattr(card, 'company', ''),
            'card_type': getattr(card, 'card_type', ''),
            'selected_category_benefits': benefits.get(selected_category, []),
            'all_benefits': benefits,
        })

    return candidate_payload


def safe_json_loads(text):
    text = text.strip()

    if text.startswith('```'):
        text = text.replace('```json', '').replace('```', '').strip()

    return json.loads(text)



def call_gemini_recommendation(
    answers,
    card_type,
    selected_category,
    category_score,
    persona,
    candidate_payload,
):
    client = genai.Client(
        api_key=os.getenv('GEMINI_API_KEY')
    )

    prompt = f"""
너는 카드 추천 서비스 '룡크크'의 AI 카드 추천 엔진이야.

사용자의 설문 결과와 후보 카드 목록을 보고,
후보 카드 목록 안에서만 사용자에게 가장 적합한 카드 3개를 추천해.

중요 규칙:
1. 반드시 후보 카드 목록에 있는 id만 골라.
2. 없는 카드명, 없는 혜택을 만들면 안 돼.
3. 사용자의 카드 유형, 소비 카테고리 점수, 선택된 소비 카테고리를 우선 반영해.
4. 추천 이유는 사용자의 설문 결과와 카드 혜택을 연결해서 설명해.
5. 응답은 반드시 JSON 객체 하나만 반환해.
6. markdown 코드블럭을 쓰지 마.

응답 형식:
{{
  "recommended_card_ids": [1, 2, 3],
  "type_reason": "왜 이 소비 유형이 나왔는지 2문장으로 설명",
  "common_benefits": "추천 카드 3개의 공통 혜택 특징을 2문장으로 요약",
  "recommend_reason": "왜 이 3개 카드를 추천했는지 전체 요약 2문장",
  "card_reasons": [
    {{
      "card_id": 1,
      "reason": "이 카드를 추천한 이유"
    }}
  ]
}}

사용자 설문 분석:
{json.dumps({
    'answers': answers,
    'card_type': card_type,
    'selected_category': selected_category,
    'category_score': category_score,
    'persona': persona,
}, ensure_ascii=False)}

후보 카드 목록:
{json.dumps(candidate_payload, ensure_ascii=False)}
"""

    response = client.models.generate_content(
        model=settings.GEMINI_MODEL,
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
        },
    )

    return safe_json_loads(response.text)