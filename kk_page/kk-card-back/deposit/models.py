from django.conf import settings
from django.db import models


class FinancialProduct(models.Model):
    PRODUCT_TYPE_CHOICES = [
        ("deposit", "정기예금"),
        ("saving", "정기적금"),
    ]

    product_type = models.CharField(
        max_length=20,
        choices=PRODUCT_TYPE_CHOICES,
    )

    # 공시 제출월
    dcls_month = models.CharField(
        max_length=6,
        blank=True,
        default="",
    )

    # 금융회사 코드
    fin_co_no = models.CharField(
        max_length=30,
    )

    # 금융회사명
    kor_co_nm = models.CharField(
        max_length=100,
    )

    # 금융상품 코드
    fin_prdt_cd = models.CharField(
        max_length=100,
    )

    # 금융상품명
    fin_prdt_nm = models.CharField(
        max_length=200,
    )

    join_way = models.TextField(
        blank=True,
        default="",
    )

    mtrt_int = models.TextField(
        blank=True,
        default="",
    )

    spcl_cnd = models.TextField(
        blank=True,
        default="",
    )

    join_deny = models.IntegerField(
        null=True,
        blank=True,
    )

    join_member = models.TextField(
        blank=True,
        default="",
    )

    etc_note = models.TextField(
        blank=True,
        default="",
    )

    max_limit = models.BigIntegerField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "product_type",
            "kor_co_nm",
            "fin_prdt_nm",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "product_type",
                    "fin_co_no",
                    "fin_prdt_cd",
                ],
                name="unique_financial_product",
            ),
        ]

    def __str__(self):
        return (
            f"{self.get_product_type_display()} / "
            f"{self.kor_co_nm} / "
            f"{self.fin_prdt_nm}"
        )


class FinancialOption(models.Model):
    product = models.ForeignKey(
        FinancialProduct,
        on_delete=models.CASCADE,
        related_name="options",
    )

    intr_rate_type = models.CharField(
        max_length=30,
        blank=True,
        default="",
    )

    intr_rate_type_nm = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    # 적금에서 사용하는 적립 방식
    rsrv_type = models.CharField(
        max_length=30,
        blank=True,
        default="",
    )

    rsrv_type_nm = models.CharField(
        max_length=100,
        blank=True,
        default="",
    )

    # 저축 기간
    save_trm = models.PositiveIntegerField()

    # 기본 금리
    intr_rate = models.FloatField(
        null=True,
        blank=True,
    )

    # 최고 우대금리
    intr_rate2 = models.FloatField(
        null=True,
        blank=True,
    )

    class Meta:
        ordering = [
            "save_trm",
            "-intr_rate2",
        ]

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "product",
                    "save_trm",
                    "intr_rate_type",
                    "rsrv_type",
                ],
                name="unique_financial_option",
            ),
        ]

    def __str__(self):
        return (
            f"{self.product.fin_prdt_nm} / "
            f"{self.save_trm}개월"
        )


class FavoriteProduct(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_financial_products",
    )

    product = models.ForeignKey(
        FinancialProduct,
        on_delete=models.CASCADE,
        related_name="favorite_links",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-id"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "product"],
                name="unique_user_favorite_product",
            ),
        ]

    def __str__(self):
        return (
            f"{self.user.username} / "
            f"{self.product.fin_prdt_nm}"
        )