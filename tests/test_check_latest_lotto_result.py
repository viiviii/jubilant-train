from datetime import date

from check_latest_lotto_result import to_message, last_sunday


def test_last_sunday():
    sunday = date(2023, 1, 1)
    monday = date(2023, 1, 2)

    assert last_sunday(today=monday) == sunday
    assert last_sunday(today=sunday) == sunday


def test_to_message():
    actual = to_message(result={
        '총 당첨금': 1234567,
        '총 구입매수': 11, '미추첨': 0,
        '시작일': date(2020, 1, 1), '종료일': date(2021, 11, 28)})

    assert actual == (
        '💰 총 당첨금: 1,234,567원\n'
        '✅ 총 구입매수: 11장 (미추첨 0장)\n'
        '📅 조회기간: 20-01-01 ~ 21-11-28')
