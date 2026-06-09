export const questions = [
  {
    id: 1,
    question: '카드 결제 금액이 빠져나가는 방식은 어떤 쪽이 더 편한가요?',
    options: [
      {
        text: '쓸 때마다 바로 빠져나가야 마음이 편해요',
        value: { key: 'card_type', value: 'check' }
      },
      {
        text: '한 달 동안 쓰고 다음 달에 한 번에 정리해도 괜찮아요',
        value: { key: 'card_type', value: 'credit' }
      }
    ]
  },
  {
    id: 2,
    question: '평소 가장 자주 돈을 쓰는 곳은 어디인가요?',
    options: [
      {
        text: '카페, 외식, 배달',
        value: { key: 'category', value: '음식/카페' }
      },
      {
        text: '온라인 쇼핑, 간편결제, 편의점',
        value: { key: 'category', value: '쇼핑/간편결제' }
      },
      {
        text: '교통, 주유, 택시',
        value: { key: 'category', value: '주유/교통' }
      },
      {
        text: 'OTT, 영화, 공연, 구독 서비스',
        value: { key: 'category', value: '문화/생활' }
      }
    ]
  },
  {
    id: 3,
    question: '온라인에서 가장 자주 결제하는 것은 무엇인가요?',
    options: [
      {
        text: '쿠팡, 무신사, 네이버쇼핑 같은 온라인 쇼핑',
        value: { key: 'category', value: '쇼핑/간편결제' }
      },
      {
        text: '배달의민족, 쿠팡이츠 같은 배달앱',
        value: { key: 'category', value: '음식/카페' }
      },
      {
        text: '넷플릭스, 유튜브, 멜론 같은 구독 서비스',
        value: { key: 'category', value: '문화/생활' }
      },
      {
        text: '구글플레이, 앱스토어 같은 인앱결제',
        value: { key: 'category', value: '결제' }
      }
    ]
  },
  {
    id: 4,
    question: '오프라인에서 자주 결제하는 곳은 어디인가요?',
    options: [
      {
        text: '카페, 음식점, 편의점',
        value: { key: 'category', value: '음식/카페' }
      },
      {
        text: '마트, 백화점, 쇼핑몰',
        value: { key: 'category', value: '쇼핑/간편결제' }
      },
      {
        text: '병원, 약국, 학원, 서점',
        value: { key: 'category', value: '교육/건강' }
      },
      {
        text: '주유소, 대중교통, 택시',
        value: { key: 'category', value: '주유/교통' }
      }
    ]
  },
  {
    id: 5,
    question: '매달 고정적으로 나가는 비용 중 가장 신경 쓰이는 것은 무엇인가요?',
    options: [
      {
        text: '통신비, 휴대폰 요금, 인터넷 요금',
        value: { key: 'category', value: '통신' }
      },
      {
        text: '관리비, 전기요금, 가스요금',
        value: { key: 'category', value: '문화/생활' }
      },
      {
        text: '구독 서비스, 멤버십, OTT',
        value: { key: 'category', value: '문화/생활' }
      },
      {
        text: '학원, 도서, 병원, 약국',
        value: { key: 'category', value: '교육/건강' }
      }
    ]
  },
  {
    id: 6,
    question: '이동할 때 어떤 소비가 가장 많나요?',
    options: [
      {
        text: '버스, 지하철 같은 대중교통',
        value: { key: 'category', value: '주유/교통' }
      },
      {
        text: '택시, 카셰어링, 주차',
        value: { key: 'category', value: '주유/교통' }
      },
      {
        text: '주유, 자동차 관련 비용',
        value: { key: 'category', value: '주유/교통' }
      },
      {
        text: '이동보다는 집 근처 생활 소비가 많아요',
        value: { key: 'category', value: '음식/카페' }
      }
    ]
  },
  {
    id: 7,
    question: '여행이나 해외 결제는 어느 정도 필요한가요?',
    options: [
      {
        text: '해외여행, 해외결제, 환전 혜택이 필요해요',
        value: { key: 'category', value: '여행' }
      },
      {
        text: '국내 숙박, 항공, 여행 플랫폼을 종종 써요',
        value: { key: 'category', value: '여행' }
      },
      {
        text: '여행보다는 일상 소비 혜택이 더 중요해요',
        value: { key: 'category', value: '음식/카페' }
      },
      {
        text: '해외보다 온라인 쇼핑 혜택이 더 필요해요',
        value: { key: 'category', value: '쇼핑/간편결제' }
      }
    ]
  },
  {
    id: 8,
    question: '혜택은 어떤 방식으로 체감되는 게 가장 좋나요?',
    options: [
      {
        text: '결제 금액에서 바로 줄어드는 할인',
        value: { key: 'benefit_keyword', value: '할인' }
      },
      {
        text: '나중에 돈처럼 돌려받는 캐시백',
        value: { key: 'benefit_keyword', value: '캐시백' }
      },
      {
        text: '포인트로 쌓이는 적립',
        value: { key: 'benefit_keyword', value: '적립' }
      },
      {
        text: '항공, 여행에 쓸 수 있는 마일리지',
        value: { key: 'benefit_keyword', value: '마일리지' }
      }
    ]
  },
  {
    id: 9,
    question: '1년에 카드 이용료가 있다면 어느 정도까지 괜찮나요?',
    options: [
      {
        text: '0원이어야 해요',
        value: { key: 'annual_fee_max', value: 0 }
      },
      {
        text: '3만원 이하까지는 괜찮아요',
        value: { key: 'annual_fee_max', value: 30000 }
      },
      {
        text: '5만원 이하까지는 괜찮아요',
        value: { key: 'annual_fee_max', value: 50000 }
      },
      {
        text: '10만원 이하까지는 괜찮아요',
        value: { key: 'annual_fee_max', value: 100000 }
      },
      {
        text: '20만원 이하까지는 괜찮아요',
        value: { key: 'annual_fee_max', value: 200000 }
      }
    ]
  },
  {
    id: 10,
    question: '본인에게 해당하는 항목이 있나요?',
    options: [
      {
        text: '특별히 해당되는 항목은 없어요',
        value: { key: 'target', value: '일반' }
      },
      {
        text: '대학생 또는 사회초년생이에요',
        value: { key: 'target', value: '대학생' }
      },
      {
        text: '개인사업자예요',
        value: { key: 'target', value: '개인사업자' }
      },
      {
        text: '군인 또는 공무원이에요',
        value: { key: 'target', value: '군인' }
      },
      {
        text: '복지/장애인 대상 혜택도 확인하고 싶어요',
        value: { key: 'target', value: '장애인' }
      }
    ]
  }
]