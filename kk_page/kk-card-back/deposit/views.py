import requests

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import (
    FavoriteProduct,
    FinancialOption,
    FinancialProduct,
)
from .serializers import (
    FinancialProductDetailSerializer,
    FinancialProductListSerializer,
)


FINLIFE_API_URLS = {
    "deposit": (
        "https://finlife.fss.or.kr/"
        "finlifeapi/depositProductsSearch.json"
    ),
    "saving": (
        "https://finlife.fss.or.kr/"
        "finlifeapi/savingProductsSearch.json"
    ),
}


def to_text(value):
    if value is None:
        return ""

    return str(value).strip()


def to_int(value):
    if value in (None, ""):
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def to_float(value):
    if value in (None, ""):
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def save_api_result(product_type, api_result):
    base_list = api_result.get("baseList", [])
    option_list = api_result.get("optionList", [])

    product_map = {}

    counts = {
        "created_products": 0,
        "updated_products": 0,
        "created_options": 0,
        "updated_options": 0,
    }

    with transaction.atomic():
        for item in base_list:
            fin_co_no = to_text(
                item.get("fin_co_no")
            )
            fin_prdt_cd = to_text(
                item.get("fin_prdt_cd")
            )

            if not fin_co_no or not fin_prdt_cd:
                continue

            product, created = (
                FinancialProduct.objects.update_or_create(
                    product_type=product_type,
                    fin_co_no=fin_co_no,
                    fin_prdt_cd=fin_prdt_cd,
                    defaults={
                        "dcls_month": to_text(
                            item.get("dcls_month")
                        ),
                        "kor_co_nm": to_text(
                            item.get("kor_co_nm")
                        ),
                        "fin_prdt_nm": to_text(
                            item.get("fin_prdt_nm")
                        ),
                        "join_way": to_text(
                            item.get("join_way")
                        ),
                        "mtrt_int": to_text(
                            item.get("mtrt_int")
                        ),
                        "spcl_cnd": to_text(
                            item.get("spcl_cnd")
                        ),
                        "join_deny": to_int(
                            item.get("join_deny")
                        ),
                        "join_member": to_text(
                            item.get("join_member")
                        ),
                        "etc_note": to_text(
                            item.get("etc_note")
                        ),
                        "max_limit": to_int(
                            item.get("max_limit")
                        ),
                    },
                )
            )

            product_map[
                (fin_co_no, fin_prdt_cd)
            ] = product

            if created:
                counts["created_products"] += 1
            else:
                counts["updated_products"] += 1

        for item in option_list:
            fin_co_no = to_text(
                item.get("fin_co_no")
            )
            fin_prdt_cd = to_text(
                item.get("fin_prdt_cd")
            )
            save_trm = to_int(
                item.get("save_trm")
            )

            if (
                not fin_co_no
                or not fin_prdt_cd
                or save_trm is None
            ):
                continue

            product = product_map.get(
                (fin_co_no, fin_prdt_cd)
            )

            if product is None:
                product = (
                    FinancialProduct.objects
                    .filter(
                        product_type=product_type,
                        fin_co_no=fin_co_no,
                        fin_prdt_cd=fin_prdt_cd,
                    )
                    .first()
                )

            if product is None:
                continue

            option, created = (
                FinancialOption.objects.update_or_create(
                    product=product,
                    save_trm=save_trm,
                    intr_rate_type=to_text(
                        item.get("intr_rate_type")
                    ),
                    rsrv_type=to_text(
                        item.get("rsrv_type")
                    ),
                    defaults={
                        "intr_rate_type_nm": to_text(
                            item.get(
                                "intr_rate_type_nm"
                            )
                        ),
                        "rsrv_type_nm": to_text(
                            item.get("rsrv_type_nm")
                        ),
                        "intr_rate": to_float(
                            item.get("intr_rate")
                        ),
                        "intr_rate2": to_float(
                            item.get("intr_rate2")
                        ),
                    },
                )
            )

            if created:
                counts["created_options"] += 1
            else:
                counts["updated_options"] += 1

    return counts


@api_view(["POST"])
def load_financial_products(request):
    api_key = settings.FINLIFE_API_KEY

    if not api_key:
        return Response(
            {
                "detail": (
                    "FINLIFE_API_KEY가 설정되지 "
                    "않았습니다."
                ),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    result_summary = {
        "deposit": {
            "created_products": 0,
            "updated_products": 0,
            "created_options": 0,
            "updated_options": 0,
        },
        "saving": {
            "created_products": 0,
            "updated_products": 0,
            "created_options": 0,
            "updated_options": 0,
        },
    }

    try:
        for product_type, api_url in (
            FINLIFE_API_URLS.items()
        ):
            page_no = 1

            while True:
                response = requests.get(
                    api_url,
                    params={
                        "auth": api_key,
                        "topFinGrpNo": "020000",
                        "pageNo": page_no,
                    },
                    timeout=20,
                )

                response.raise_for_status()

                response_data = response.json()
                api_result = response_data.get(
                    "result",
                    {},
                )

                page_counts = save_api_result(
                    product_type,
                    api_result,
                )

                for key, value in page_counts.items():
                    result_summary[
                        product_type
                    ][key] += value

                max_page_no = (
                    to_int(
                        api_result.get(
                            "max_page_no"
                        )
                    )
                    or page_no
                )

                if page_no >= max_page_no:
                    break

                page_no += 1

    except requests.RequestException as error:
        return Response(
            {
                "detail": (
                    "금융감독원 API 호출에 "
                    "실패했습니다."
                ),
                "error": str(error),
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    except ValueError as error:
        return Response(
            {
                "detail": (
                    "금융감독원 API 응답을 "
                    "해석하지 못했습니다."
                ),
                "error": str(error),
            },
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response(
        {
            "detail": (
                "예적금 데이터 저장이 "
                "완료되었습니다."
            ),
            "result": result_summary,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def financial_product_list(request):
    products = (
        FinancialProduct.objects
        .prefetch_related("options")
        .all()
    )

    product_type = request.query_params.get(
        "product_type",
        "",
    )
    bank = request.query_params.get(
        "bank",
        "",
    )
    term = request.query_params.get(
        "term",
        "",
    )
    search = request.query_params.get(
        "search",
        "",
    )

    if product_type in ("deposit", "saving"):
        products = products.filter(
            product_type=product_type
        )

    if bank:
        products = products.filter(
            kor_co_nm=bank
        )

    if term:
        term_value = to_int(term)

        if term_value is not None:
            products = products.filter(
                options__save_trm=term_value
            )

    if search:
        products = products.filter(
            Q(fin_prdt_nm__icontains=search)
            | Q(kor_co_nm__icontains=search)
        )

    products = products.distinct()

    serializer = FinancialProductListSerializer(
        products,
        many=True,
        context={"request": request},
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def financial_product_detail(
    request,
    product_pk,
):
    product = get_object_or_404(
        FinancialProduct.objects.prefetch_related(
            "options"
        ),
        id=product_pk,
    )

    serializer = FinancialProductDetailSerializer(
        product,
        context={"request": request},
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def toggle_favorite_product(
    request,
    product_pk,
):
    product = get_object_or_404(
        FinancialProduct,
        id=product_pk,
    )

    favorite, created = (
        FavoriteProduct.objects.get_or_create(
            user=request.user,
            product=product,
        )
    )

    if created:
        return Response(
            {
                "detail": (
                    "관심 상품에 추가되었습니다."
                ),
                "is_favorite": True,
            },
            status=status.HTTP_201_CREATED,
        )

    favorite.delete()

    return Response(
        {
            "detail": (
                "관심 상품에서 삭제되었습니다."
            ),
            "is_favorite": False,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def favorite_product_list(request):
    products = (
        FinancialProduct.objects
        .filter(
            favorite_links__user=request.user
        )
        .prefetch_related("options")
        .distinct()
    )

    serializer = FinancialProductListSerializer(
        products,
        many=True,
        context={"request": request},
    )

    return Response(
        serializer.data,
        status=status.HTTP_200_OK,
    )