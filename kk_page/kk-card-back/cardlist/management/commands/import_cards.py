import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from cardlist.models import Card


class Command(BaseCommand):
    help = "Import card JSON files into database"

    def handle(self, *args, **kwargs):
        data_dir = Path(settings.BASE_DIR) / "data"

        if not data_dir.exists():
            self.stdout.write(self.style.ERROR(f"data 폴더가 없습니다: {data_dir}"))
            return

        json_files = list(data_dir.glob("*.json"))

        if not json_files:
            self.stdout.write(self.style.ERROR("JSON 파일이 없습니다."))
            return

        total_count = 0

        for json_file in json_files:
            self.stdout.write(f"읽는 중: {json_file.name}")

            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # JSON 구조가 리스트인 경우
            if isinstance(data, list):
                cards = data

            # JSON 구조가 {"cards": [...]} 인 경우
            elif isinstance(data, dict) and "cards" in data:
                cards = data["cards"]

            else:
                self.stdout.write(
                    self.style.WARNING(f"{json_file.name} 형식 확인 필요")
                )
                continue

            for item in cards:
                company = item.get("company", "")
                name = item.get("name", "")

                if not name:
                    continue

                Card.objects.update_or_create(
                    company=company,
                    name=name,
                    defaults={
                        "card_type": item.get("card_type", ""),
                        "target": item.get("target", ""),
                        "annual_fee": item.get("annual_fee", {}),
                        "benefits": item.get("benefits", {}),
                        "image_url": item.get("image_url", ""),
                        "detail_url": item.get("detail_url", ""),
                    },
                )

                total_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"카드 데이터 DB 저장 완료: {total_count}개")
        )