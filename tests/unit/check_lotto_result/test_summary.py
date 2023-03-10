import pytest

from check_lotto_result.summary import group_by_round, prize_to_int, Summary


def test_group_by_round():
    buys = [
        # 회차 1054
        {'구입일자': '2023-02-07', '복권명': '로또6/45', '회차': '1054', '선택번호/복권번호': '51738 11491 27411 72232 76893 71219',
         '구입매수': '1', '당첨결과': '미추첨', '당첨금': '-', '추첨일': '2023-02-11'},
        # 회차 1053
        {'구입일자': '2023-02-04', '복권명': '로또6/45', '회차': '1053', '선택번호/복권번호': '50012 91499 11223 13078 24189 31090',
         '구입매수': '1', '당첨결과': '당첨', '당첨금': '50,000원', '추첨일': '2023-02-04'},
        {'구입일자': '2023-02-03', '복권명': '로또6/45', '회차': '1053', '선택번호/복권번호': '59912 84214 97899 66707 11366 52190',
         '구입매수': '10', '당첨결과': '낙첨', '당첨금': '-', '추첨일': '2023-02-04'},
        {'구입일자': '2023-02-02', '복권명': '로또6/45', '회차': '1053', '선택번호/복권번호': '51234 23523 25939 66117 14366 66190',
         '구입매수': '100', '당첨결과': '당첨', '당첨금': '5,000원', '추첨일': '2023-02-04'},
    ]

    actual = group_by_round(buys)

    assert actual == [
        Summary(round='1054', draw_date='2023-02-11', prize=0, quantity=1),
        Summary(round='1053', draw_date='2023-02-04', prize=55000, quantity=111)
    ]


@pytest.mark.parametrize(
    'prize, expected',
    [('', 0), ('-', 0), ('1,000원', 1000), ('$1,234,567', 1234567)]
)
def test_prize_to_int(prize, expected):
    assert prize_to_int(prize) == expected
