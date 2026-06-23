from rest_framework import serializers
from .models import Card
from .models import RecommendResult

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = "__all__"


class ResultSerializer(serializers.ModelSerializer):
    # 저장할 때 Vue에서 카드 ID 3개를 받는 필드
    card_ids = serializers.PrimaryKeyRelatedField(
        queryset=Card.objects.all(),
        source="card_list",
        many=True,
        write_only=True,
    )

    # 조회할 때 카드명, 이미지 등 카드 전체 정보를 반환
    recommended_cards = CardSerializer(
        source="card_list",
        many=True,
        read_only=True,
    )

    # 사용자는 요청을 보낸 로그인 사용자로 자동 저장
    user = serializers.ReadOnlyField(
        source="user.username",
    )

    class Meta:
        model = RecommendResult
        fields = [
            "id",
            "persona_title",
            "persona_description",
            "card_ids",
            "recommended_cards",
            "user",
        ]

    def validate_card_ids(self, cards):
        if len(cards) != 3:
            raise serializers.ValidationError(
                "추천 카드 3개를 저장해야 합니다."
            )

        return cards
