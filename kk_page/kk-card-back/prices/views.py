import pandas as pd
from pathlib import Path

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


DATA_FILES = {
    'gold': 'Gold_prices.xlsx',
    'silver': 'Silver_prices.xlsx',
}


def load_price_data(asset):
    file_name = DATA_FILES.get(asset)

    if not file_name:
        raise ValueError('잘못된 자산 타입입니다.')

    file_path = Path(settings.BASE_DIR) / 'data' / file_name

    df = pd.read_excel(file_path)

    # 컬럼명 공백 제거
    df.columns = [str(col).strip() for col in df.columns]

    # 현재 엑셀 기준:
    # Date, Close/Last, Volume, Open, High, Low
    df = df[['Date', 'Close/Last']]

    # 프론트에서 쓰기 쉽게 컬럼명 변경
    df.columns = ['date', 'price']

    # 날짜 변환
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # 가격 변환
    # 혹시 $24.562 또는 1,234.56 이런 식으로 되어 있어도 처리
    df['price'] = (
        df['price']
        .astype(str)
        .str.replace('$', '', regex=False)
        .str.replace(',', '', regex=False)
    )

    df['price'] = pd.to_numeric(df['price'], errors='coerce')

    # 날짜나 가격이 비어있는 행 제거
    df = df.dropna(subset=['date', 'price'])

    # 날짜순 정렬
    df = df.sort_values('date')

    return df


@api_view(['GET'])
def price_chart(request):
    asset = request.GET.get('asset', 'gold')
    start = request.GET.get('start')
    end = request.GET.get('end')

    if asset not in ['gold', 'silver']:
        return Response(
            {'message': 'asset은 gold 또는 silver만 가능합니다.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        df = load_price_data(asset)

        start_date = pd.to_datetime(start) if start else None
        end_date = pd.to_datetime(end) if end else None

        # 잘못된 날짜 선택
        if start_date is not None and end_date is not None:
            if start_date > end_date:
                return Response(
                    {'message': '시작일은 종료일보다 늦을 수 없습니다.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # 시작일 필터
        if start_date is not None:
            df = df[df['date'] >= start_date]

        # 종료일 필터
        if end_date is not None:
            df = df[df['date'] <= end_date]

        # 해당 기간 데이터 없음
        if df.empty:
            return Response({
                'asset': asset,
                'labels': [],
                'prices': [],
                'message': '선택한 기간에 해당하는 데이터가 없습니다.'
            })

        labels = df['date'].dt.strftime('%Y-%m-%d').tolist()
        prices = df['price'].tolist()

        return Response({
            'asset': asset,
            'labels': labels,
            'prices': prices,
            'message': ''
        })

    except KeyError:
        return Response(
            {
                'message': '엑셀 파일에 Date 또는 Close/Last 컬럼이 없습니다.'
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    except Exception as e:
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
