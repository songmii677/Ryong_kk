import json
import os

from django.conf import settings
from google import genai

CATEGORY_WEIGHT = {
    '기타': 0.6,
}

TARGET_GROUP_MAP = {
    '사업자': ['사업자', '개인사업자', '법인', '지방보조금 보조사업자'],
    '특정지역': ['특정지역'],
    '프리미엄': ['프리미엄', '별도의 카드 가입 자격 심사'],
    '공공/복지': ['군인', '공무원', '소방', '장애인', '국민연금 수급자'],
}

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
    target_group = None

    for answer in answers:
        key = answer.get('key')
        value = answer.get('value')

        if key == 'card_type':
            card_type = value

        if key == 'category':
            category_score[value] = category_score.get(value, 0) + 1

        if key == 'target_group':
            target_group = value

    selected_category = None

    if category_score:
        selected_category = sorted(
            category_score.items(),
            key=lambda item: item[1] * CATEGORY_WEIGHT.get(item[0], 1),
            reverse=True
        )[0][0]

    return {
        'card_type': card_type,
        'selected_category': selected_category,
        'category_score': category_score,
        'target_group': target_group,
    }


def get_persona(category):
    if category == '음식/카페':
        return {
            'title': '☕ 취향을 채우는 미식형',
            'desc': '맛있는 순간과 여유로운 시간을 통해 일상의 만족을 높이는 타입',
        }

    if category == '통신':
        return {
            'title': '📱 루틴을 정리하는 실속형',
            'desc': '매달 반복되는 생활 비용을 놓치지 않고 관리하는 타입',
        }

    if category == '쇼핑/간편결제':
        return {
            'title': '🛍️ 감각적인 선택형',
            'desc': '필요한 순간에 빠르게 고르고, 편리한 결제를 선호하는 타입',
        }

    if category == '주유/교통':
        return {
            'title': '🚕 동선을 아끼는 효율형',
            'desc': '이동 시간과 비용까지 똑똑하게 계산하는 타입',
        }

    if category == '교육/건강':
        return {
            'title': '🌿 나를 돌보는 성장형',
            'desc': '건강과 자기계발처럼 오래 남는 가치에 투자하는 타입',
        }

    if category == '여행':
        return {
            'title': '✈️ 경험을 넓히는 탐색형',
            'desc': '익숙한 일상 밖에서 새로운 순간과 경험을 찾는 타입',
        }

    if category == '문화/생활':
        return {
            'title': '🎧 일상을 즐기는 취향형',
            'desc': '콘텐츠, 취미, 생활 속 즐거움으로 하루를 채우는 타입',
        }

    if category == '기타':
        return {
            'title': '✨ 어디서나 챙기는 균형형',
            'desc': '특정 영역보다 전체 결제에서 꾸준한 혜택을 선호하는 타입',
        }

    return {
        'title': '🌱 균형 잡힌 실속형',
        'desc': '여러 생활 영역을 고르게 챙기며 안정적인 혜택을 선호하는 타입',
    }


def get_candidate_cards(
    Card,
    card_type,
    selected_category,
    category_score,
    target_group=None,
    limit=30,
):
    queryset = Card.objects.filter(card_type=card_type)

    scored_cards = []

    for card in queryset:
        benefits = normalize_benefits(getattr(card, 'benefits', {}))

        score = 0

        for category, count in category_score.items():
            category_benefits = benefits.get(category, [])
            weight = CATEGORY_WEIGHT.get(category, 1)

            if category_benefits:
                score += count * 3 * weight
                score += min(len(category_benefits), 5) * weight

        if selected_category and benefits.get(selected_category):
            selected_weight = CATEGORY_WEIGHT.get(selected_category, 1)
            score += 5 * selected_weight

        if target_group:
            target_values = TARGET_GROUP_MAP.get(target_group, [])
            card_target = getattr(card, 'target', '')

            if card_target in target_values:
                score += 4

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

역할:
사용자의 설문 결과와 후보 카드 목록을 보고,
후보 카드 안에서만 가장 잘 맞는 카드 3개를 골라.

추천 기준:
- 사용자가 선택한 카드 유형을 우선 반영해.
- 가장 많이 선택된 생활 패턴과 카드 혜택이 잘 맞는지 확인해.
- 같은 혜택이 반복되면 더 구체적인 카드 혜택을 가진 카드를 우선해.
- 후보 카드 목록에 없는 카드명이나 혜택은 절대 만들지 마.

문장 스타일:
- 결과 화면에 바로 보여줄 문구로 작성해.
- 각 설명은 2문장으로 작성해.
- 너무 짧은 한 줄 요약으로 끝내지 마.
- 단, 한 항목은 80~120자 정도로 유지해.
- 첫 문장은 사용자의 성향을 말하고, 두 번째 문장은 카드 혜택과 연결해.
- “소비 카테고리”, “점수”, “데이터” 같은 분석 용어는 쓰지 마.
- 사용자가 심리테스트 결과를 보는 느낌으로 작성해.
- 존댓말 대신 부드러운 안내형 문장으로 써.

응답 규칙:
1. 반드시 후보 카드 목록에 있는 id만 골라.
2. 추천 카드는 정확히 3개만 골라.
3. 응답은 JSON 객체 하나만 반환해.
4. markdown 코드블럭을 쓰지 마.
5. 모든 문장은 한국어로 작성해.

응답 형식:
{{
  "recommended_card_ids": [1, 2, 3],
  "type_reason": "사용자 유형을 2문장으로 설명. 첫 문장은 성향, 두 번째 문장은 선택한 생활 패턴과 연결",
  "common_benefits": "추천 카드들의 공통 혜택을 2문장으로 설명. 구체적인 혜택 키워드를 포함",
  "recommend_reason": "이 3장을 고른 이유를 2문장으로 설명. 사용자의 성향과 카드 혜택이 어떻게 맞는지 포함",
  "card_reasons": [
    {{
      "card_id": 1,
      "reason": "카드별 추천 이유를 50~70자 정도로 작성"
    }}
  ]
}}

좋은 예시:
{{
  "type_reason": "자주 쓰는 생활 영역에서 바로 체감되는 혜택을 선호하는 타입이야.",
  "common_benefits": "세 카드 모두 일상 결제에서 부담을 줄여주는 혜택이 강해.",
  "recommend_reason": "선택한 생활 패턴과 혜택 구성이 가장 자연스럽게 맞는 카드들이야.",
  "card_reasons": [
    {{
      "card_id": 1,
      "reason": "자주 쓰는 영역의 할인 혜택이 뚜렷해."
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