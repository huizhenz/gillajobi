"""
python backend/competitions/test_crawlers_manual.py
"""
import unittest
from datetime import date

from crawlers import ACTIVE_STATUSES, crawl_page, parse_period, parse_status


class TestParsePeriod(unittest.TestCase):
    def test_normal(self):
        start, end = parse_period("26-06-17 ~ 26-08-26")
        self.assertEqual(start, date(2026, 6, 17))
        self.assertEqual(end, date(2026, 8, 26))

    def test_invalid(self):
        start, end = parse_period("날짜없음")
        self.assertIsNone(start)
        self.assertIsNone(end)

    def test_empty(self):
        start, end = parse_period("")
        self.assertIsNone(start)
        self.assertIsNone(end)


class TestParseStatus(unittest.TestCase):
    def test_접수중(self):
        self.assertEqual(parse_status("접수중D-69"), "접수중")

    def test_마감임박(self):
        self.assertEqual(parse_status("마감임박D-3"), "마감임박")

    def test_접수예정(self):
        self.assertEqual(parse_status("접수예정"), "접수예정")

    def test_마감(self):
        self.assertEqual(parse_status("마감"), "마감")

    def test_unknown(self):
        self.assertEqual(parse_status("알수없음"), "알수없음")


class TestCrawlPage(unittest.TestCase):
    def test_page1_returns_results(self):
        results = crawl_page(1)
        self.assertIsInstance(results, list)
        print(f"\n[page 1] {len(results)}개 수집")
        if results:
            print("첫 번째 항목:", results[0])

    def test_result_keys(self):
        results = crawl_page(1)
        if not results:
            self.skipTest("크롤링 결과 없음 (네트워크 확인)")
        expected_keys = {"external_id", "title", "host", "start_date", "end_date", "status", "detail_url"}
        self.assertEqual(set(results[0].keys()), expected_keys)

    def test_active_statuses_exist(self):
        results = crawl_page(1)
        if not results:
            self.skipTest("크롤링 결과 없음 (네트워크 확인)")
        active = [r for r in results if r["status"] in ACTIVE_STATUSES]
        print(f"\n활성 공모전: {len(active)}개 / 전체: {len(results)}개")
        self.assertGreater(len(active), 0)

    def test_invalid_page_returns_empty(self):
        results = crawl_page(99999)
        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
