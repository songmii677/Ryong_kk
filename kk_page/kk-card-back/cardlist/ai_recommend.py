import json
import os

from django.conf import settings
from openai import OpenAI
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


def get_persona(card_type, category):
    if card_type == 'check' and category == '음식/카페':
        return {
            'title': '☕ 카페 러버',
            'desc': '카페와 외식, 배달을 즐기는 소비형',
        }

    if card_type == 'check' and category == '통신':
        return {
            'title': '💸 알뜰한 생활러',
            'desc': '고정 지출을 아끼는 실속형',
        }

    if card_type == 'credit' and category == '쇼핑/간편결제':
        return {
            'title': '🛍️ 혜택 사냥꾼',
            'desc': '쇼핑 할인과 적립을 적극 활용하는 타입',
        }

    if card_type == 'credit' and category == '여행':
        return {
            'title': '✈️ 여행 준비러',
            'desc': '항공과 숙박 혜택을 중요하게 생각하는 타입',
        }

    if card_type == 'credit' and category == '문화/생활':
        return {
            'title': '🎬 OTT 마스터',
            'desc': '넷플릭스와 구독 서비스를 즐기는 타입',
        }

    return {
        'title': '🌱 사회초년생',
        'desc': '실속 있는 소비를 추구하는 타입',
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