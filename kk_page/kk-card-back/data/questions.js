export const questions = [
  {
    id: 1,
    question: '어떤 카드를 찾고 있나요?',
    options: [
      { text: '부담 없이 쓰는 체크카드', value: { key: 'card_type', value: 'check' } },
      { text: '혜택이 더 다양한 신용카드', value: { key: 'card_type', value: 'credit' } }
    ]
  },
  {
    id: 2,
    question: '가장 자주 쓰는 소비 영역은?',
    options: [
      { text: '카페, 외식, 배달', value: { key: 'category', value: '음식/카페' } },
      { text: '쇼핑, 간편결제, 온라인몰', value: { key: 'category', value: '쇼핑/간편결제' } }
    ]
  },
  {
    id: 3,
    question: '평소 더 많이 쓰는 고정비는?',
    options: [
      { text: '교통비, 주유비', value: { key: 'category', value: '주유/교통' } },
      { text: '통신비, 구독 서비스', value: { key: 'category', value: '통신' } }
    ]
  },
  {
    id: 4,
    question: '쉬는 날에는 주로 뭘 하나요?',
    options: [
      { text: '영화, OTT, 공연을 즐겨요', value: { key: 'category', value: '문화/생활' } },
      { text: '여행이나 해외 결제에 관심 있어요', value: { key: 'category', value: '여행' } }
    ]
  },
  {
    id: 5,
    question: '어떤 혜택 방식이 더 좋아요?',
    options: [
      { text: '바로 할인되는 혜택', value: { key: 'benefit_keyword', value: '할인' } },
      { text: '포인트가 쌓이는 혜택', value: { key: 'benefit_keyword', value: '적립' } }
    ]
  },
  {
    id: 6,
    question: '연회비는 어느 쪽이 좋아요?',
    options: [
      { text: '연회비 없는 카드가 좋아요', value: { key: 'fee', value: 'free' } },
      { text: '혜택이 좋으면 연회비 있어도 괜찮아요', value: { key: 'fee', value: 'any' } }
    ]
  },
  {
    id: 7,
    question: '온라인 소비를 자주 하나요?',
    options: [
      { text: '온라인 쇼핑, 배달앱을 자주 써요', value: { key: 'category', value: '쇼핑/간편결제' } },
      { text: '오프라인 결제를 더 자주 해요', value: { key: 'benefit_keyword', value: '할인' } }
    ]
  },
  {
    id: 8,
    question: '카드를 고를 때 더 중요한 건?',
    options: [
      { text: '복잡하지 않은 기본 혜택', value: { key: 'simple', value: 'simple' } },
      { text: '조건이 있어도 큰 혜택', value: { key: 'simple', value: 'premium' } }
    ]
  },
  {
    id: 9,
    question: '주로 어디에서 결제하나요?',
    options: [
      { text: '편의점, 카페, 음식점', value: { key: 'category', value: '음식/카페' } },
      { text: '마트, 쇼핑몰, 온라인몰', value: { key: 'category', value: '쇼핑/간편결제' } }
    ]
  },
  {
    id: 10,
    question: '나는 어떤 소비자에 가까운가요?',
    options: [
      { text: '소소하게 자주 쓰는 편', value: { key: 'type', value: 'daily' } },
      { text: '한 번 쓸 때 크게 쓰는 편', value: { key: 'type', value: 'big_spender' } }
    ]
  }
]