from django_filters import rest_framework as filters

from .models import Card


class CardFilter(filters.FilterSet):
    CARD_TYPE_CHOICES = [
        ("credit", "신용카드"),
        ("check", "체크카드"),
    ]

    COMPANY_CHOICES = [
        ("삼성", "삼성카드"),
        ("하나", "하나카드"),
        ("국민", "국민카드"),
        ("신한카드", "신한카드"),
        ("우리카드", "우리카드"),
    ]

    card_type = filters.ChoiceFilter(
        field_name="card_type",
        choices=CARD_TYPE_CHOICES,
    )

    company = filters.ChoiceFilter(
        field_name="company",
        choices=COMPANY_CHOICES,
    )

    card_name = filters.CharFilter(
        field_name="name",
        lookup_expr="icontains"
    )

    class Meta:
        model = Card
        fields = [
            "card_type",
            "company",
            "card_name",
        ]