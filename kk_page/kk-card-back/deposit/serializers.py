from rest_framework import serializers

from .models import (
    FinancialOption,
    FinancialProduct,
)


class FinancialOptionSerializer(
    serializers.ModelSerializer
):
    class Meta:
        model = FinancialOption
        fields = [
            "id",
            "intr_rate_type",
            "intr_rate_type_nm",
            "rsrv_type",
            "rsrv_type_nm",
            "save_trm",
            "intr_rate",
            "intr_rate2",
        ]


class FavoriteStatusMixin:
    def get_is_favorite(self, obj):
        request = self.context.get("request")

        if (
            request is None
            or not request.user.is_authenticated
        ):
            return False

        return obj.favorite_links.filter(
            user=request.user
        ).exists()


class FinancialProductListSerializer(
    FavoriteStatusMixin,
    serializers.ModelSerializer,
):
    rates = serializers.SerializerMethodField()
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = FinancialProduct
        fields = [
            "id",
            "product_type",
            "dcls_month",
            "fin_co_no",
            "kor_co_nm",
            "fin_prdt_cd",
            "fin_prdt_nm",
            "rates",
            "is_favorite",
        ]

    def get_rates(self, obj):
        rates = {}

        for option in obj.options.all():
            term = str(option.save_trm)

            current_value = (
                option.intr_rate2
                if option.intr_rate2 is not None
                else option.intr_rate
            )

            existing = rates.get(term)

            if existing is not None:
                existing_value = (
                    existing["max"]
                    if existing["max"] is not None
                    else existing["basic"]
                )

                if (
                    current_value is None
                    or (
                        existing_value is not None
                        and current_value
                        <= existing_value
                    )
                ):
                    continue

            rates[term] = {
                "basic": option.intr_rate,
                "max": option.intr_rate2,
            }

        return rates


class FinancialProductDetailSerializer(
    FavoriteStatusMixin,
    serializers.ModelSerializer,
):
    product_type_name = serializers.CharField(
        source="get_product_type_display",
        read_only=True,
    )

    options = FinancialOptionSerializer(
        many=True,
        read_only=True,
    )

    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = FinancialProduct
        fields = [
            "id",
            "product_type",
            "product_type_name",
            "dcls_month",
            "fin_co_no",
            "kor_co_nm",
            "fin_prdt_cd",
            "fin_prdt_nm",
            "join_way",
            "mtrt_int",
            "spcl_cnd",
            "join_deny",
            "join_member",
            "etc_note",
            "max_limit",
            "options",
            "is_favorite",
        ]