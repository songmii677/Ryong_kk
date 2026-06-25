export const questions = [
  {
    id: 1,
    question: '하늘에서 100만원이 떨어졌다(야르)! 이 돈을 어떻게 다룰까?',
    options: [
      {
        text: '쓸 돈을 미리 나눠두고 바로바로 확인한다',
        value: { key: 'card_type', value: 'check' }
      },
      {
        text: '일단 흐름에 맡기고, 나중에 한 번에 정리한다',
        value: { key: 'card_type', value: 'credit' }
      }
    ]
  },
  {
    id: 2,
    question: '완전히 비어 있는 토요일, 나에게 자유이용권을 준다면?',
    options: [
      {
        text: '새로 생긴 공간에서 맛있는 걸 먹으며 쉬고 싶다',
        value: { key: 'category', value: '음식/카페' }
      },
      {
        text: '마음속 장바구니에 넣어둔 것들을 구경하고 싶다',
        value: { key: 'category', value: '쇼핑/간편결제' }
      },
      {
        text: '보고 싶던 영화, 전시, 콘텐츠를 몰아서 즐기고 싶다',
        value: { key: 'category', value: '문화/생활' }
      },
      {
        text: '장소를 정하지 않고 어디서든 무난하게 쓰고 싶다',
        value: { key: 'category', value: '기타' }
      }
    ]
  },
  {
    id: 3,
    question: '친구가 오늘 하루 코스를 전부 맡긴다면, 나는 무엇부터 챙길까?',
    options: [
      {
        text: '시작은 분위기 좋은 한 끼가 중요하다',
        value: { key: 'category', value: '음식/카페' }
      },
      {
        text: '환승 적고 편하게 움직이는 동선이 중요하다',
        value: { key: 'category', value: '주유/교통' }
      },
      {
        text: '근처에 쇼핑이나 구경할 곳이 있으면 좋다',
        value: { key: 'category', value: '쇼핑/간편결제' }
      },
      {
        text: '영화, 전시, 공연처럼 기억에 남는 일정이 필요하다',
        value: { key: 'category', value: '문화/생활' }
      }
    ]
  },
  {
    id: 4,
    question: '하루가 길었던 날, 나에게 작은 보상을 준다면?',
    options: [
      {
        text: '달달한 한입이나 맛있는 한 끼로 기분을 풀고 싶다',
        value: { key: 'category', value: '음식/카페' }
      },
      {
        text: '미뤄뒀던 필요한 아이템을 하나 사고 싶다',
        value: { key: 'category', value: '쇼핑/간편결제' }
      },
      {
        text: '몸 상태나 컨디션을 제대로 챙기고 싶다',
        value: { key: 'category', value: '교육/건강' }
      },
      {
        text: '어디에 쓰든 조금씩 돌아오는 안정감이 좋다',
        value: { key: 'category', value: '기타' }
      }
    ]
  },
  {
    id: 5,
    question: '내 돈... 어디 갔지? 가장 신경 쓰이는 고정 지출은?',
    options: [
      {
        text: '휴대폰, 인터넷처럼 매달 빠져나가는 필수 요금',
        value: { key: 'category', value: '통신' }
      },
      {
        text: '영상, 음악, 멤버십처럼 하나둘 쌓이는 구독 비용',
        value: { key: 'category', value: '문화/생활' }
      },
      {
        text: '데이터가 느리거나 연락이 안 돼서 답답할 때',
        value: { key: 'category', value: '통신' }
      },
      {
        text: '딱히 하나만 고르기보다 전체 결제에서 새는 돈',
        value: { key: 'category', value: '기타' }
      }
    ]
  },
  {
    id: 6,
    question: '오늘 하루의 동선이 갑자기 꼬였다! 내가 제일 예민해지는 순간은?',
    options: [
      {
        text: '늦지 않게 움직이느라 이동비가 늘어날 때',
        value: { key: 'category', value: '주유/교통' }
      },
      {
        text: '급하게 필요한 걸 사야 하는데 결제가 번거로울 때',
        value: { key: 'category', value: '쇼핑/간편결제' }
      },
      {
        text: '갑자기 멀리 가거나 예약을 잡아야 할 때',
        value: { key: 'category', value: '여행' }
      },
      {
        text: '데이터, 통화, 연결이 끊겨서 일이 막힐 때',
        value: { key: 'category', value: '통신' }
      }
    ]
  },
  {
    id: 7,
    question: '지도 앱을 켰는데 마음이 살짝 들뜬다. 내가 먼저 눌러보는 건?',
    options: [
      {
        text: '낯선 도시, 공항, 숙소처럼 새로운 장소',
        value: { key: 'category', value: '여행' }
      },
      {
        text: '어디서 쓰든 조금씩 쌓이는 기본 혜택',
        value: { key: 'category', value: '기타' }
      },
      {
        text: '멀리 돌아가지 않는 가장 편한 이동 루트',
        value: { key: 'category', value: '주유/교통' }
      },
      {
        text: '오늘 볼 수 있는 전시, 영화, 공연 일정',
        value: { key: 'category', value: '문화/생활' }
      }
    ]
  },
  {
    id: 8,
    question: '룡크크가 선물을 준다면 어떤 방식이 제일 좋을까?',
    options: [
      {
        text: '지금 바로 가격이 줄어드는 선물',
        value: { key: 'benefit_keyword', value: '할인' }
      },
      {
        text: '나중에 현금처럼 돌아오는 선물',
        value: { key: 'benefit_keyword', value: '캐시백' }
      },
      {
        text: '차곡차곡 쌓여서 나중에 쓰는 선물',
        value: { key: 'benefit_keyword', value: '적립' }
      },
      {
        text: '멀리 떠날 때 크게 도움 되는 선물',
        value: { key: 'benefit_keyword', value: '마일리지' }
      }
    ]
  },
  {
    id: 9,
    question: '마음에 드는 멤버십을 발견했다. 1년에 어느 정도까지 괜찮을까?',
    options: [
      {
        text: '무료가 아니면 살짝 망설여진다',
        value: { key: 'annual_fee_max', value: 0 }
      },
      {
        text: '혜택이 보이면 3만원 이하는 괜찮다',
        value: { key: 'annual_fee_max', value: 30000 }
      },
      {
        text: '확실히 돌려받는 게 있으면 5만원까지 가능하다',
        value: { key: 'annual_fee_max', value: 50000 }
      },
      {
        text: '혜택이 크다면 10만원대도 고려할 수 있다',
        value: { key: 'annual_fee_max', value: 100000 }
      }
    ]
  },
  {
    id: 10,
    question: '미래의 나에게 선물 하나를 보낸다면?',
    options: [
      {
        text: '몸과 마음의 컨디션을 챙기는 선물',
        value: { key: 'category', value: '교육/건강' }
      },
      {
        text: '낯선 곳에서도 여유롭게 움직일 수 있는 선물',
        value: { key: 'category', value: '여행' }
      },
      {
        text: '작은 행복을 바로 충전해주는 선물',
        value: { key: 'category', value: '음식/카페' }
      },
      {
        text: '매일 끊김 없이 연결되는 생활 기반',
        value: { key: 'category', value: '통신' }
      }
    ]
  },
  {
    id: 11,
    question: '마지막으로, 더 잘 맞는 카드를 찾기 위해 가까운 쪽을 골라줘!',
    options: [
      {
        text: '특별한 조건 없이 누구나 쓰기 좋은 카드가 좋아요',
        value: { key: 'target', value: '일반' }
      },
      {
        text: '사업이나 업무 지출에 도움 되는 혜택도 보고 싶어요',
        value: { key: 'target_group', value: '사업자' }
      },
      {
        text: '특정 지역이나 제휴 기반 혜택도 괜찮아요',
        value: { key: 'target_group', value: '특정지역' }
      },
      {
        text: '연회비가 있어도 프리미엄 혜택이 크면 좋아요',
        value: { key: 'target_group', value: '프리미엄' }
      },
      {
        text: '공공/복지/군인/공무원 관련 혜택도 확인하고 싶어요',
        value: { key: 'target_group', value: '공공/복지' }
      }
    ]
  }
]