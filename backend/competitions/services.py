from competitions.crawlers import crawl_all
from competitions.models import Competition

def sync_competitions():
    results = crawl_all()
    total_saved = 0

    for r in results:
        if r["external_id"] is None:
            continue
        try:
            Competition.objects.update_or_create(
                external_id=r["external_id"],
                defaults={
                    "title": r["title"],
                    "host": r["host"],
                    "start_date": r["start_date"],
                    "end_date": r["end_date"],
                    "status": r["status"],
                    "detail_url": r["detail_url"],
                }
            )
            total_saved += 1
        except Exception as e:
            print(f"DB 저장 오류 (external_id={r['external_id']}): {e}. 건너뜀.")

    print(f"\n총 {total_saved}개 저장 완료")
    return total_saved
