import re
from datetime import datetime
import calendar

def identify_beautiful_sequences_with_positions(sim_number):
    # Định nghĩa các mẫu dãy số đẹp, bổ sung các quy tắc mới
    patterns = {
        "AAA.AAA.AAA": r"(\d)\1{8}",
        "ABCDE.ABCDE": r"(\d)(\d)(\d)(\d)(\d)\1\2\3\4\5",
        "AB.AB.AB.AB.AB": r"(\d)(\d)\1\2\1\2\1\2\1\2",
        "ABCDE.EDCBA": r"(\d)(\d)(\d)(\d)(\d)\5\4\3\2\1",
        "ABCDE.ABCDE⁺¹": r"(\d)(\d)(\d)(\d)(\d)\1\2\3\4(\d)",
        "ABCDE.ABCD⁺¹E": r"(\d)(\d)(\d)(\d)(\d)\1\2\3(\d)\5",
        "ABCDE.ABC⁺¹DE": r"(\d)(\d)(\d)(\d)(\d)\1\2(\d)\4\5",
        "ABCDE.AB⁺¹CDE": r"(\d)(\d)(\d)(\d)(\d)\1(\d)\3\4\5",
        "ABCDE.A⁺¹BCDE": r"(\d)(\d)(\d)(\d)(\d)(\d)\2\3\4\5",
        "ABBBB.ACCCC": r"(\d)(\d)\2{3}\1(\d)\3{3}",
        "ABCDE.FBCDE": r"(\d)(\d)(\d)(\d)(\d)(\d)\2\3\4\5",
        "ABCDE.AFCDE": r"(\d)(\d)(\d)(\d)(\d)\1(\d)\3\4\5",
        "ABCDE.ABFDE": r"(\d)(\d)(\d)(\d)(\d)\1\2(\d)\4\5",
        "ABCDE.ABCFE": r"(\d)(\d)(\d)(\d)(\d)\1\2\3(\d)\5",
        "ABCDE.ABCDF": r"(\d)(\d)(\d)(\d)(\d)\1\2\3\4(\d)",
        "AB.AC.AD.AE.AF": r"(\d)(\d)\1(\d)\1(\d)\1(\d)\1(\d)",
        "AB.CB.DB.EB.FB": r"(\d)(\d)(\d)\2(\d)\2(\d)\2(\d)\2",
        "ABCDE.ABCDE⁻¹": r"(\d)(\d)(\d)(\d)(\d)\1\2\3\4(\d)",
        "ABCDE.ABCD⁻¹E": r"(\d)(\d)(\d)(\d)(\d)\1\2\3(\d)\5",
        "ABCDE.ABC⁻¹DE": r"(\d)(\d)(\d)(\d)(\d)\1\2(\d)\4\5",
        "ABCDE.AB⁻¹CDE": r"(\d)(\d)(\d)(\d)(\d)\1(\d)\3\4\5",
        "ABCDE.A⁻¹BCDE": r"(\d)(\d)(\d)(\d)(\d)(\d)\2\3\4\5",
        "AAAA.AAAA": r"(\d)\1{7}",
        "DD.MM.YYYY": r"(\d){8}",
        "ABC.ABC.ABC": r"(\d)(\d)(\d)\1\2\3\1\2\3",
        "AAA.BBB.CCC": r"(\d)\1\1(\d)\2\2(\d)\3\3",
        "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶A⁺⁷A⁺⁸A⁺⁹": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "3.4.5.6.7.8.9.10": r"345678910",
        "97.98.99.100": r"979899100",
        "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶A⁻⁷A⁻⁸A⁻⁹": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "AAAAAAA": r"(\d)\1{6}",
        "ABCD.ABCD": r"((\d)(\d)(\d)(\d)\2\3\4\5)",
        "AB.AB.AB.AB": r"(\d)(\d)\1\2\1\2\1\2",
        "AA.BB.CC.DD": r"(\d)\1(\d)\2(\d)\3(\d)\4",
        "AAAA.BBBB": r"(\d)\1\1\1(\d)\2\2\2",
        "ABCD.DCBA": r"(\d)(\d)(\d)(\d)\4\3\2\1",
        "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶A⁺⁷A⁺⁸": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "ABCD.ABCD⁺¹": r"(\d)(\d)(\d)(\d)\1\2\3(\d)",
        "ABCD.ABC⁺¹D": r"(\d)(\d)(\d)(\d)\1\2(\d)\4",
        "ABCD.AB⁺¹CD": r"(\d)(\d)(\d)(\d)\1(\d)\3\4",
        "ABCD.A⁺¹BCD": r"(\d)(\d)(\d)(\d)(\d)\2\3\4",
        "4.5.6.7.8.9.10": r"45678910",
        "ABBB.ACCC": r"(\d)(\d)\2\2\1(\d)\3\3",
        "AAAB.AAAC": r"(\d)\1\1(\d)\1\1(\d)",
        "ABCD.EBCD": r"(\d)(\d)(\d)(\d)(\d)\2\3\4",
        "ABCD.AECD": r"(\d)(\d)(\d)(\d)\1(\d)\3\4",
        "ABCD.ABED": r"(\d)(\d)(\d)(\d)\1\2(\d)\4",
        "ABCD.ABCE": r"(\d)(\d)(\d)(\d)\1\2\3(\d)",
        "ABAC.ADAE": r"(\d)(\d)\1(\d)\1(\d)\1(\d)",
        "AB.CB.DB.EB": r"(\d)(\d)(\d)\2(\d)\2(\d)\2",
        "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶A⁻⁷A⁻⁸": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "ABCD.ABCD⁻¹": r"(\d)(\d)(\d)(\d)\1\2\3(\d)",
        "ABCD.ABC⁻¹D": r"(\d)(\d)(\d)(\d)\1\2(\d)\4",
        "ABCD.AB⁻¹CD": r"(\d)(\d)(\d)(\d)\1(\d)\3\4",
        "ABCD.A⁻¹BCD": r"(\d)(\d)(\d)(\d)(\d)\2\3\4",
        "AAA.AAA": r"(\d)\1{5}",
        "DD.MM.YY": r"(\d){6}",
        "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶A⁺⁷": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "5.6.7.8.9.10": r"5678910",
        "98.99.100": r"9899100",
        "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶A⁻⁷": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "AA.A⁺¹A⁺¹.A⁺²A⁺²": r"(\d)\1(\d)\2(\d)\3",
        "AA.A⁺²A⁺².A⁺⁴A⁺⁴": r"(\d)\1(\d)\2(\d)\3",
        "AA.A⁻¹A⁻¹.A⁻²A⁻²": r"(\d)\1(\d)\2(\d)\3",
        "AA.A⁻²A⁻².A⁻⁴A⁻⁴": r"(\d)\1(\d)\2(\d)\3",
        "AAAAA": r"(\d)\1{4}",
        "ABC.ABC": r"(\d)(\d)(\d)\1\2\3",
        "AB.AB⁻¹.AB⁻²": r"(\d)(\d)\1(\d)\1(\d)",
        "AB.A⁻¹B.A⁻²B": r"(\d)(\d)(\d)\2(\d)\2",
        "AB.AB.AB": r"(\d)(\d)\1\2\1\2",
        "AA.BB.CC": r"(\d)\1(\d)\2(\d)\3",
        "AAA.BBB": r"(\d)\1\1(\d)\2\2",
        "ABC.CBA": r"(\d)(\d)(\d)\3\2\1",
        "ABC.ABC⁺¹": r"(\d)(\d)(\d)\1\2(\d)",
        "ABC.AB⁺¹C": r"(\d)(\d)(\d)\1(\d)\3",
        "ABC.A⁺¹BC": r"(\d)(\d)(\d)(\d)\2\3",
        "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶": r'(?=(\d{6}))',
        "9.10.11.12.13": r"910111213",
        "6.7.8.9.10.11": r"67891011",
        "8.9.10.11.12": r"89101112",
        "6.7.8.9.10.11": r"67891011",
        "9.10.11.12": r"9101112",
        "9.10.11.12": r"9101112",
        "7.8.9.10.11": r"7891011",
        "6.7.8.9.10": r"678910",
        "8.9.10.11": r"891011",
        "ABB.ACC": r"(\d)(\d)\2\1(\d)\3",
        "AAB.AAC": r"(\d)\1(\d)\1\1(\d)",
        "ACC.BCC": r"(\d)(\d)\2(\d)\2\2",
        "ABC.DBC": r"(\d)(\d)(\d)(\d)\2\3",
        "AB⁺¹.AB⁺².AB⁺³": r"(\d)(\d)\1(\d)\1(\d)",
        "AB.AC.AD": r"(\d)(\d)\1(\d)\1(\d)",
        "AB.A⁺¹B.A⁺²B": r"(\d(\d)(\d)\2(\d)\2)",
        "AB.CB.DB": r"(\d(\d)(\d)\2(\d)\2)",
        "ABC.ABD": r"(\d)(\d)(\d)\1\2(\d)",
        "ABC.ADC": r"(\d)(\d)(\d)\1(\d)\3",
        "ABC.ABC⁻¹": r"(\d)(\d)(\d)\1\2(\d)",
        "ABC.AB⁻¹C": r"(\d)(\d)(\d)\1(\d)\3",
        "ABC.A⁻¹BC": r"(\d)(\d)(\d)(\d)\2\3",
        "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶": r"(\d{6})",
        "AAAA": r"(\d)\1{3}",
        "YYYY": r"(\d){4}",
        "ABXBA": r"(\d)(\d)(\d)\2\1",
        "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵": r'(?=(\d{5}))',
        "AA⁺²A⁺⁴A⁺⁶A⁺⁸": r"13579",
        "AA⁺²A⁺⁴A⁺⁶A⁺⁸": r"02468",
        "7.8.9.10": r"78910",
        "9.10.11": r"91011",
        "99.100": r"99100",
        "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵": r"(\d{5})",
        "AA⁻²A⁻⁴A⁻⁶A⁻⁸": r"97531",
        "AA⁻²A⁻⁴A⁻⁶A⁻⁸": r"86420",
        "AAA": r"(\d{3})",
        "ABAB": r"(\d)(\d)\1\2",
        "AA.A⁺¹A⁺¹": r"(\d)\1(\d)\2",
        "AABB": r"(\d)\1(\d)\2",
        "ABBA": r"(\d)(\d)\2\1",
        "AB.AB⁺¹": r"(\d)(\d)\1(\d)",
        "ABA⁺¹B": r"(\d)(\d)(\d)\2",
        "A⁺¹A⁺²A⁺³A⁺⁴": r"(\d{4})",
        "AA⁺²A⁺⁴A⁺⁶": r"(\d{4})",
        "AAAD+": r"8910",
        "ABAC": r"((\d)\d\2\d)",
        "ABCB": r"(\d(\d)\d\2)",
        "ABAB⁻¹": r"(\d)(\d)\1(\d)",
        "ABA⁻¹B": r"(\d)(\d)(\d)\2",
        "A⁻¹A⁻²A⁻³A⁻⁴": r"(\d{4})",
        "AA⁻²A⁻⁴A⁻⁶": r"(\d{4})",
        "AA": r"(\d)\1",
        "AXA": r"(\d)(\d)\1",
        "A⁺¹A⁺²A⁺³": r"(\d{3})",
        "AA⁺²A⁺⁴": r"(\d{3})",
        "A⁻¹A⁻²A⁻³": r"(\d{3})",
        "AA⁻²A⁻⁴": r"(\d{3})",
        "A⁺¹A⁺²": r"(\d{2})"
    }
    
    patterns_middle = {
        "AAAA.AAAA": r"(\d)\1{7}",
        "DD.MM.YYYY": r'(?=(\d{8}))',
        "AAAAAAA": r"(\d)\1{6}",
        "ABCD.ABCD": r"((\d)(\d)(\d)(\d)\2\3\4\5)",
        "AB.AB.AB.AB": r"(\d)(\d)\1\2\1\2\1\2",
        "AA.BB.CC.DD": r"(\d)\1(\d)\2(\d)\3(\d)\4",
        "AAAA.BBBB": r"(\d)\1\1\1(\d)\2\2\2",
        "ABCD.DCBA": r"(\d)(\d)(\d)(\d)\4\3\2\1",
        "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶A⁺⁷A⁺⁸": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "ABCD.ABCD⁺¹": r"(\d)(\d)(\d)(\d)\1\2\3(\d)",
        "ABCD.ABC⁺¹D": r"(\d)(\d)(\d)(\d)\1\2(\d)\4",
        "ABCD.AB⁺¹CD": r"(\d)(\d)(\d)(\d)\1(\d)\3\4",
        "ABCD.A⁺¹BCD": r"(\d)(\d)(\d)(\d)(\d)\2\3\4",
        "45678910": r"(45678910)",
        "ABBB.ACCC": r"(\d)(\d)\2\2\1(\d)\3\3",
        "AAAB.AAAC": r"(\d)\1\1(\d)\1\1(\d)",
        "ABCD.EBCD": r"(\d)(\d)(\d)(\d)(\d)\2\3\4",
        "ABCD.AECD": r"(\d)(\d)(\d)(\d)\1(\d)\3\4",
        "ABCD.ABED": r"(\d)(\d)(\d)(\d)\1\2(\d)\4",
        "ABCD.ABCE": r"(\d)(\d)(\d)(\d)\1\2\3(\d)",
        "ABACADAE": r"(?=((\d)\d\2\d\2\d\2\d))",
        "AB.CB.DB.EB": r"(\d(\d)\d\2\d\2\d\2)",
        "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶A⁻⁷A⁻⁸": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "ABCD.ABCD⁻¹": r"(\d)(\d)(\d)(\d)\1\2\3(\d)",
        "ABCD.ABC⁻¹D": r"(\d)(\d)(\d)(\d)\1\2(\d)\4",
        "ABCD.AB⁻¹CD": r"(\d)(\d)(\d)(\d)\1(\d)\3\4",
        "ABCD.A⁻¹BCD": r"(\d)(\d)(\d)(\d)(\d)\2\3\4",
        "AAA.AAA": r"(\d)\1{5}",
        "DD.MM.YY": r'(?=(\d{6}))',
        "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶A⁺⁷": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "5.6.7.8.9.10": r"(5678910)",
        "98.99.100": r"(9899100)",
        "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶A⁻⁷": r"(\d)(\d)(\d)(\d)(\d)(\d)(\d)",
        "AA.A⁺¹A⁺¹.A⁺²A⁺²": r"((\d)\2(\d)\3(\d)\4)",
        "AA.A⁺²A⁺².A⁺⁴A⁺⁴": r"((\d)\2(\d)\3(\d)\4)",
        "AA.A⁻¹A⁻¹.A⁻²A⁻²": r"((\d)\2(\d)\3(\d)\4)",
        "AA.A⁻²A⁻².A⁻⁴A⁻⁴": r"((\d)\2(\d)\3(\d)\4)",
        "AAAAA": r"(\d)\1{4}",
        "ABC.ABC": r"(\d)(\d)(\d)\1\2\3",
        "AB.AB⁻¹.AB⁻²": r"((\d)\d\2\d\2\d)",
        "AB.A⁻¹B.A⁻²B": r"(\d(\d)\d\2\d\2)",
        "AB.AB.AB": r"(\d)(\d)\1\2\1\2",
        "AA.BB.CC": r'(?=((\d)\2(\d)\3(\d)\4))',
        "AAA.BBB": r"(\d)\1\1(\d)\2\2",
        "ABC.CBA": r"(?=((\d)(\d)(\d)\4\3\2))",
        "ABC.ABC⁺¹": r"(\d)(\d)(\d)\1\2(\d)",
        "ABC.AB⁺¹C": r"(\d)(\d)(\d)\1(\d)\3",
        "ABC.A⁺¹BC": r"(\d)(\d)(\d)(\d)\2\3",
        "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶": r'(?=(\d{6}))',
        "6.7.8.9.10": r"(678910)",
        "ABB.ACC": r"(\d)(\d)\2\1(\d)\3",
        "AAB.AAC": r"(\d)\1(\d)\1\1(\d)",
        "ACC.BCC": r"(\d)(\d)\2(\d)\2\2",
        "ABC.DBC": r"(\d)(\d)(\d)(\d)\2\3",
        "AB⁺¹.AB⁺².AB⁺³": r"(\d)(\d)\1(\d)\1(\d)",
        "AB.AC.AD": r"(\d)(\d)\1(\d)\1(\d)",
        "AB.A⁺¹B.A⁺²B": r"(\d(\d)(\d)\2(\d)\2)",
        "AB.CB.DB": r"(?=(\d(\d)(\d)\2(\d)\2))",
        "ABC.ABD": r"(\d)(\d)(\d)\1\2(\d)",
        "ABC.ADC": r"(\d)(\d)(\d)\1(\d)\3",
        "ABC.ABC⁻¹": r"(?=((\d)(\d)\d\2\3\d))",
        "ABC.AB⁻¹C": r"(?=((\d)\d(\d)\2\d\3))",
        "ABC.A⁻¹BC": r"(?=(\d(\d)(\d)\d\2\3))",
        "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶": r'(?=(\d{6}))',
        "AAAA": r"(\d)\1{3}",
        "YYYY": r'(?=(\d{3}))',
        "ABXBA": r"(?=((\d)(\d)\d\3\2))",
        "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵": r'(?=(\d{5}))',
        "AA⁺²A⁺⁴A⁺⁶A⁺⁸": r"13579",
        "AA⁺²A⁺⁴A⁺⁶A⁺⁸": r"02468",
        "9.10.11.12.13": r"(910111213)",
        "6.7.8.9.10.11": r"(67891011)",
        "8.9.10.11.12": r"(89101112)",
        "6.7.8.9.10.11": r"(67891011)",
        "9.10.11.12": r"(9101112)",
        "9.10.11.12": r"(9101112)",
        "7.8.9.10.11": r"(7891011)",
        "6.7.8.9.10": r"(678910)",
        "8.9.10.11": r"(891011)",
        "7.8.9.10": r"(78910)",
        "9.10.11": r"(91011)",
        "99.100": r"(99100)",
        "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵": r'(?=(\d{5}))',
        "AA⁻²A⁻⁴A⁻⁶A⁻⁸": r"(97531)",
        "AA⁻²A⁻⁴A⁻⁶A⁻⁸": r"(86420)",
        "AAA": r'(?=(\d{3}))',
        "ABAB": r"(\d)(\d)\1\2",
        "AA.A⁺¹A⁺¹": r'(?=(\d{4}))',
        "AABB": r'(?=(\d{4}))',
        "ABBA": r'(?=(\d{4}))',
        "ABAB⁺¹": r"(\d)(\d)\1(\d)",
        "ABA⁺¹B": r"(\d)(\d)(\d)\2",
        "A⁺¹A⁺²A⁺³A⁺⁴": r'(?=(\d{4}))',
        "AA⁺²A⁺⁴A⁺⁶": r'(?=(\d{4}))',
        "AAAD+": r"(8910)",
        "ABAC": r"(?=((\d)\d\2\d))",
        "ABCB": r"(?=(\d(\d)\d\2))",
        "AB.AB⁻¹": r"(?=((\d)\d\2\d))",
        "AB.A⁻¹B": r"(\d)(\d)(\d)\2",
        "A⁻¹A⁻²A⁻³A⁻⁴": r'(?=(\d{4}))',
        "AA⁻²A⁻⁴A⁻⁶": r'(?=(\d{4}))',
        "AA": r'(?=((\d)\2))',
        "AXA": r"(\d)(\d)\1",
        "A⁺¹A⁺²A⁺³": r'(?=(\d{3}))',
        "AA⁺²A⁺⁴": r'(?=(\d{3}))',
        "A⁻¹A⁻²A⁻³": r'(?=(\d{3}))',
        "AA⁻²A⁻⁴": r'(?=(\d{3}))',
        "A⁺¹A⁺²": r'(?=(\d{2}))',
    }
    
    detail_number = ['14078', '15078', '0102', '0404', '0378', '1102', '1204', '2204', '4078', '4404', '1369', '1618', '2204', '8386', '1368', '1569', '4078', '6688', '0578', '4953', '2283', '1486', '1919', '6879', '6679', '6979', '3689', '6689', '1689', '2368', '2628', '2626', '2828', '365', '389', '569', '688', '866', '69', '96', '68', '86', '39', '79', '38', '78', '18', '16', '36', '83']

    # Chuẩn hóa số sim bằng cách loại bỏ các ký tự không phải số
    if not isinstance(sim_number, str):
        sim_number = str(sim_number) if sim_number is not None else ''
    sim_number = re.sub(r'\D', '', sim_number)
    
    sim_number_backup = sim_number

    # Danh sách kết quả
    result = {
        "Dạng đẹp đầu": "",
        "Dãy đẹp đầu": "",
        "Vị trí đầu": "",
        "Dạng đẹp giữa": [],
        "Dãy đẹp giữa": [],
        "Vị trí giữa": [],
        "Dạng đẹp đuôi": "",
        "Dãy đẹp đuôi": "",
        "Vị trí đuôi": ""
    }

    def is_valid_pattern(pattern_name, sequence):
      match pattern_name:
          case "YYYY":
            current_year = datetime.now().year
            try:
                sequence = int(sequence)
                if 1950 <= sequence <= current_year + 1:
                    return True
            except ValueError:
                # Xử lý nếu sequence không thể chuyển đổi thành int
                print("Giá trị của sequence không hợp lệ")
            return False
          case "DD.MM.YYYY":
             # Kiểm tra độ dài của chuỗi
            if len(sequence) != 8:
                return False
            
            # Tách thành ngày, tháng, và năm
            dd = int(sequence[:2])
            mm = int(sequence[2:4])
            yyyy = int(sequence[4:])
            
            # Kiểm tra năm hợp lệ
            current_year = datetime.now().year
            if not (1950 <= yyyy <= current_year):
                return False

            # Kiểm tra tháng hợp lệ
            if not (1 <= mm <= 12):
                return False
            
            # Kiểm tra ngày hợp lệ cho tháng đã cho
            max_day = calendar.monthrange(yyyy, mm)[1]  # Số ngày tối đa cho tháng này
            if not (1 <= dd <= max_day):
                return False
            
            # Nếu tất cả đều hợp lệ, trả về True
            return True
          case "DD.MM.YY":
            if len(sequence) != 6:
                return False

            # Tách ngày, tháng, và năm
            dd = int(sequence[:2])
            mm = int(sequence[2:4])
            yy = int(sequence[4:])
            
            # Xác định năm đầy đủ từ YY
            current_year = datetime.now().year
            if 50 <= yy <= 99:
                yyyy = 1900 + yy
            elif 0 <= yy <= current_year % 100:
                yyyy = 2000 + yy
            else:
                return False
            
            # Kiểm tra tháng hợp lệ
            if not (1 <= mm <= 12):
                return False
            
            # Kiểm tra ngày hợp lệ cho tháng đã cho
            max_day = calendar.monthrange(yyyy, mm)[1]
            if not (1 <= dd <= max_day):
                return False
            
            # Nếu tất cả đều hợp lệ, trả về True
            return True
          case "AAA":
            return len(sequence) == 3 and sequence[0] == sequence[1] == sequence[2]
          case "ABCB":
            return len(sequence) == 4 and count_type_number(sequence) >= 2
          case "ABA⁻¹B":
            return len(sequence) == 4 and int(sequence[0]) == int(sequence[2]) + 1 and count_type_number(sequence) == 3
          case "ABAB⁻¹":
            return len(sequence) == 4 and int(sequence[1]) == int(sequence[3]) + 1
          case "A⁺¹A⁺²A⁺³":
            if len(sequence) != 3:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) + 1:
                  return False
      
            return True
          case "A⁻¹A⁻²A⁻³":
            if len(sequence) != 3:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) - 1:
                  return False
      
            return True
          case "AA⁺²A⁺⁴":
            if len(sequence) != 3:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) + 2:
                  return False
      
            return True
          case "AA⁻²A⁻⁴":
            if len(sequence) != 3:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) - 2:
                  return False
      
            return True
          case "AA⁺²A⁺⁴A⁺⁶":
            if len(sequence) != 4:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) + 2:
                  return False
      
            return True
          case "AA⁻²A⁻⁴A⁻⁶":
            if len(sequence) != 4:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) - 2:
                  return False
      
            return True
          case "A⁻¹A⁻²A⁻³A⁻⁴":
            if len(sequence) != 4:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) - 1:
                  return False
      
            return True
          case "A⁺¹A⁺²A⁺³A⁺⁴":
            if len(sequence) != 4:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) + 1:
                  return False
      
            return True
          case "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵":
            if len(sequence) != 5:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) - 1:
                  return False
      
            return True
          case "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵":
            if len(sequence) != 5:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) + 1:
                  return False
      
            return True
          case "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶":
            if len(sequence) != 6:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) - 1:
                  return False
      
            return True
          case "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶":
            if len(sequence) != 6:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) + 1:
                  return False
      
            return True
          case "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶A⁻⁷":
            if len(sequence) != 7:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) - 1:
                  return False
      
            return True
          case "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶A⁺⁷":
            if len(sequence) != 7:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) + 1:
                  return False
      
            return True
          case "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶A⁻⁷A⁻⁸":
            if len(sequence) != 8:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) - 1:
                  return False
      
            return True
          case "AB.AB⁻¹.AB⁻²":
            return len(sequence) == 6 and int(sequence[1]) == int(sequence[3]) + 1 and int(sequence[3]) == int(sequence[5]) + 1
          case "AB.A⁻¹B.A⁻²B":
            return len(sequence) == 6 and int(sequence[0]) == int(sequence[2]) + 1 and int(sequence[2]) == int(sequence[4]) + 1
          case "AA.A⁺¹A⁺¹.A⁺²A⁺²":
            return len(sequence) == 6 and int(sequence[0]) == int(sequence[2]) - 1 and int(sequence[2]) == int(sequence[4]) - 1
          case "AA.A⁺²A⁺².A⁺⁴A⁺⁴":
            return len(sequence) == 6 and int(sequence[0]) == int(sequence[2]) - 2 and int(sequence[2]) == int(sequence[4]) - 2
          case "AA.A⁻²A⁻².A⁻⁴A⁻⁴":
            return len(sequence) == 6 and int(sequence[0]) == int(sequence[2]) + 2 and int(sequence[2]) == int(sequence[4]) + 2
          case "AA.A⁻¹A⁻¹.A⁻²A⁻²":
            return len(sequence) == 6 and int(sequence[0]) == int(sequence[2]) + 1 and int(sequence[2]) == int(sequence[4]) + 1
          case "ABCD.ABCD⁺¹":
            return len(sequence) == 8 and int(sequence[3]) == int(sequence[7]) - 1
          case "ABCD.ABC⁺¹D":
            return len(sequence) == 8 and int(sequence[2]) == int(sequence[6]) - 1
          case "ABCD.AB⁺¹CD":
            return len(sequence) == 8 and int(sequence[1]) == int(sequence[5]) - 1
          case "ABCD.A⁺¹BCD":
            return len(sequence) == 8 and int(sequence[0]) == int(sequence[4]) - 1
          case "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶A⁺⁷A⁺⁸":
            if len(sequence) != 8:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) + 1:
                  return False
      
            return True
          case "A⁺¹A⁺²A⁺³A⁺⁴A⁺⁵A⁺⁶A⁺⁷A⁺⁸A⁺⁹":
            if len(sequence) != 9:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) + 1:
                  return False
      
            return True
          case "A⁻¹A⁻²A⁻³A⁻⁴A⁻⁵A⁻⁶A⁻⁷A⁻⁸A⁻⁹":
            if len(sequence) != 9:
              return False
          
            for i in range(1, len(sequence)):
              if int(sequence[i]) != int(sequence[i-1]) - 1:
                  return False
      
            return True
          case "AA.BB.CC":
            return count_type_number(sequence) == 3 and int(sequence[0]) == int(sequence[1]) and int(sequence[2]) == int(sequence[3]) and int(sequence[4]) == int(sequence[5])
          case "AABB":
            return count_type_number(sequence) == 2 and int(sequence[1]) == int(sequence[0]) and int(sequence[2]) == int(sequence[3])
          case "ABC.B⁺¹C":
            return count_type_number(sequence) >= 3 and int(sequence[1]) == int(sequence[4]) + 1
          case "AA.A⁺¹A⁺¹":
            return count_type_number(sequence) == 2 and int(sequence[1]) == int(sequence[0]) and int(sequence[2]) == int(sequence[3]) and int(sequence[1]) == int(sequence[2]) - 1
          case "ABBA":
            return count_type_number(sequence) == 2 and int(sequence[0]) == int(sequence[3]) and int(sequence[1]) == int(sequence[2])
          case "ABAC":
            return len(sequence) == 4 and count_type_number(sequence) >= 2
          case "A⁺¹A⁺²":
            return len(sequence) == 2 and int(sequence[1]) == int(sequence[0]) + 1  # Kiểm tra điều kiện AA1
          case "ABAB⁺¹":
            return len(sequence) == 4 and count_type_number(sequence) == 3 and int(sequence[3]) == int(sequence[1]) + 1  
          case "ABA⁺¹B":
            return len(sequence) == 4 and (int(sequence[2]) == int(sequence[0]) + 1)
          case "ABCDE.EDCBA":
            return len(sequence) == 10 and count_type_number(sequence) == 5
          case "ABCDE.AB⁺¹CDE":
            return count_type_number(sequence) >=5 and int(sequence[1]) + 1 == int(sequence[6])
          case "ABCD.ABCD":
            return len(sequence) == 8 and count_type_number(sequence) >= 3
          case "AAAB.AAAC":
            return len(sequence) == 8 and count_type_number(sequence) == 3
          case "ABCD.ABCE":
            return len(sequence) == 8 and count_type_number(sequence) == 5
          case "ABCD.AECD":
            return len(sequence) == 8 and count_type_number(sequence) == 5
          case "ABCDE.A⁺¹BCDE":
            return len(sequence) == 10 and count_type_number(sequence) >=5  and int(sequence[0]) + 1 == int(sequence[5])
          case "ABACADAE":
            return len(sequence) == 8 and count_type_number(sequence) >= 3
          case "ABCD.ABCD⁻¹":
            return len(sequence) == 8 and count_type_number(sequence) == 5 and int(sequence[3]) - 1 == int(sequence[7])
          case "ABCD.AB⁻¹CD":
            return len(sequence) == 8 and count_type_number(sequence) == 5 and int(sequence[1]) == int(sequence[5]) + 1
          case "ABCD.EBCD":
            return len(sequence) == 8 and count_type_number(sequence) == 5
          case "ABCDE.ABCDE":
            return len(sequence) == 10 and count_type_number(sequence) == 5
          case "ABCDE.FBCDE":
            return len(sequence) == 10 and count_type_number(sequence) == 6
          case "ABCD.A⁻¹BCD":
            return len(sequence) == 8 and count_type_number(sequence) == 5 and int(sequence[0]) - 1 == int(sequence[4])
          case "ABCD.ABED": 
            return len(sequence) == 8 and count_type_number(sequence) == 5
          case "AB.CB.DB.EB":
            return len(sequence) == 8 and count_type_number(sequence) >= 3
          case "AB.CB.DB":
            return len(sequence) == 6 and count_type_number(sequence) >= 2
          case "ABCA⁺¹BC":
            return len(sequence) == 6 and count_type_number(sequence) == 4 and int(sequence[0]) == int(sequence[3]) - 1
          case "ABCD.ABC⁻¹D":
            return len(sequence) == 8 and count_type_number(sequence) == 5 and int(sequence[2]) - 1 == int(sequence[6])
          case "ABC.ABC⁺¹":
            return len(sequence) == 6 and count_type_number(sequence) == 4 and int(sequence[2]) + 1 == int(sequence[5])
          case "ABC.AB⁺¹C":
            return len(sequence) == 6 and int(sequence[1]) == int(sequence[1]) - 1
          case "AB.AC.AD":
            return len(sequence) == 6 and count_type_number(sequence) >= 3
          case "AB⁺¹.AB⁺².AB⁺³":
            return len(sequence) == 6 and int(sequence[1]) == int(sequence[3]) - 1 and int(sequence[3]) == int(sequence[5]) - 1
          case "ACC.BCC":
            return len(sequence) == 6 and count_type_number(sequence) == 3
          case "ABC.A⁺¹BC":
            return len(sequence) == 6 and count_type_number(sequence) == 4 and int(sequence[1]) + 1 == int(sequence[4])
          case "ABCDE.ABCD⁺¹E":
            return len(sequence) == 10 and count_type_number(sequence) >= 5  and int(sequence[3]) + 1 == int(sequence[8])
          case "AA.BB.CC.DD":
            return len(sequence) == 8 and count_type_number(sequence) == 4
          case "ABC.DBC":
            return len(sequence) == 6 and count_type_number(sequence) == 4
          case "AB.A⁺¹B.A⁺²B":
            return len(sequence) == 6 and int(sequence[0]) == int(sequence[2]) - 1 and int(sequence[2]) == int(sequence[4]) - 1
          case "ABCDE.ABC⁺¹DE":
            return len(sequence) == 10 and count_type_number(sequence) >= 5 and int(sequence[2]) + 1 == int(sequence[7])
          case "ABXBA":
            return len(sequence) == 5 and count_type_number(sequence) >= 2
          case "ABC.ADC":
            return len(sequence) == 6 and count_type_number(sequence) == 4
          case "ABBBB.ACCCC":
            return len(sequence) == 10 and count_type_number(sequence) == 3
          case "ABCA⁻¹BC":
            return len(sequence) == 6 and (count_type_number(sequence) == 4 or count_type_number(sequence) == 3) and int(sequence[0]) - 1 == int(sequence[3])
          case "ABC.AB⁻¹C":
            return len(sequence) == 6 and (count_type_number(sequence) == 4 or count_type_number(sequence) == 3) and int(sequence[1]) - 1 == int(sequence[4])
          case "ABC.ABC⁻¹":
            return len(sequence) == 6 and (count_type_number(sequence) == 4 or count_type_number(sequence) == 3) and int(sequence[2]) - 1 == int(sequence[5])
          case "ABCDE.ABCDE⁺¹":        
            return len(sequence) == 10 and count_type_number(sequence) >= 4 and int(sequence[4]) == int(sequence[9]) - 1
          case "ABCDE.ABCDE⁻¹":        
            return len(sequence) == 10 and count_type_number(sequence) >= 4 and int(sequence[4]) == int(sequence[9]) + 1
          case "ABCDE.ABCD⁻¹E":        
            return len(sequence) == 10 and count_type_number(sequence) >= 4 and int(sequence[3]) == int(sequence[8]) + 1
          case "ABCDE.ABC⁻¹DE":        
            return len(sequence) == 10 and count_type_number(sequence) >= 4 and int(sequence[2]) == int(sequence[7]) + 1
          case "ABCDE.AB⁻¹CDE":        
            return len(sequence) == 10 and count_type_number(sequence) >= 4 and int(sequence[1]) == int(sequence[6]) + 1
          case "ABCDE.A⁻¹BCDE":        
            return len(sequence) == 10 and count_type_number(sequence) >= 4 and int(sequence[0]) == int(sequence[5]) + 1
          case _:
              return True
    # Tìm dãy số đẹp ở đuôi
    # for pattern_name, pattern in sorted(patterns.items(), key=lambda x: -len(x[1])):  # Ưu tiên các mẫu dài nhất
    tail_mode = True  # Bắt đầu tìm từ đuôi
    while len(sim_number) > 1:
        found_beautiful_segment = False

        # Tìm các mẫu dãy đẹp từ patterns
        for pattern_name, pattern in patterns.items():
            match = re.search(pattern + r'$', sim_number)
            if match and is_valid_pattern(pattern_name, match.group()):
                if tail_mode:
                    # Lưu dãy đẹp ở đuôi
                    result["Dạng đẹp đuôi"] = pattern_name
                    result["Dãy đẹp đuôi"] = match.group()
                    result["Vị trí đuôi"] = len(sim_number) - len(match.group())
                    tail_mode = False  # Chuyển sang tìm giữa
                else:
                    # Kiểm tra nếu dãy đẹp nằm ở đầu
                    if sim_number.startswith(match.group()):
                        result["Dạng đẹp đầu"] = pattern_name
                        result["Dãy đẹp đầu"] = match.group()
                        result["Vị trí đầu"] = 0
                    else:
                        # Lưu dãy đẹp ở giữa
                        result["Dạng đẹp giữa"].append(pattern_name)
                        result["Dãy đẹp giữa"].append(match.group())
                        result["Vị trí giữa"].append(len(sim_number) - len(match.group()))
                sim_number = sim_number[:-len(match.group())]  # Cắt phần đã xét
                found_beautiful_segment = True
                break

        # Nếu không tìm thấy dãy đẹp nào từ patterns
        if not found_beautiful_segment:
            for length in range(5, 1, -1):
                if length > len(sim_number):
                    continue
                end_segment = sim_number[-length:]
                if end_segment in detail_number:
                    if tail_mode:
                        # Lưu dãy đẹp ở đuôi khi đang ở tail_mode
                        result["Dạng đẹp đuôi"] = "DB"
                        result["Dãy đẹp đuôi"] = end_segment
                        result["Vị trí đuôi"] = len(sim_number) - length
                        tail_mode = False
                    else:
                        # Kiểm tra nếu dãy đẹp nằm ở đầu
                        if sim_number.startswith(end_segment):
                            result["Dạng đẹp đầu"] = "DB"
                            result["Dãy đẹp đầu"] = end_segment
                            result["Vị trí đầu"] = 0
                        else:
                            # Lưu dãy đẹp ở giữa
                            result["Dạng đẹp giữa"].append("DB")
                            result["Dãy đẹp giữa"].append(end_segment)
                            result["Vị trí giữa"].append(len(sim_number) - length)
                    sim_number = sim_number[:-length]
                    found_beautiful_segment = True
                    break

        # Dừng vòng lặp nếu không tìm thấy dãy đẹp nào
        if not found_beautiful_segment:
            break


    # Tìm dãy số đẹp ở đầu
    if len(sim_number) > 1:
      for pattern_name, pattern in patterns.items():
          match = re.match(pattern, sim_number)
          if match and is_valid_pattern(pattern_name, match.group()):
              result["Dạng đẹp đầu"] = pattern_name
              result["Dãy đẹp đầu"] = match.group()
              result["Vị trí đầu"] = 0
              sim_number = sim_number[len(match.group()):]  # Loại bỏ dãy đẹp đầu
              break
      if result["Dãy đẹp đầu"] == "":  
          for size in range(5, 1, -1):
              start_segment = sim_number[:size]
              # Kiểm tra nếu start_segment không phải là chuỗi trống
              if start_segment and start_segment.isdigit():
                  if start_segment in detail_number:
                      result["Dạng đẹp đầu"] = "DB"
                      result["Dãy đẹp đầu"] = start_segment
                      result["Vị trí đầu"] = 0
                      sim_number = sim_number[size:]  # Loại bỏ dãy số đã đối chiếu
                      break

    # Tìm các dãy số đẹp còn lại từ trái sang phải
    current_position = 0
    
    while sim_number:
        max_length = 0
        max_pattern_name = ""
        max_sequence = ""
        max_start_pos = -1

        # Duyệt qua tất cả các mẫu, ưu tiên theo độ dài hoặc ưu tiên bạn muốn
        for pattern_name, pattern in patterns_middle.items():
            matches = list(re.finditer(pattern, sim_number))
            for m in matches:
                matched_string = m.group(1)
                start_pos = m.start()

                # Kiểm tra xem dãy có dài hơn dãy trước không và có khớp với điều kiện hợp lệ không
                if len(matched_string) > max_length and is_valid_pattern(pattern_name, matched_string):
                    max_length = len(matched_string)
                    max_pattern_name = pattern_name
                    max_sequence = matched_string
                    max_start_pos = start_pos

        # Nếu không tìm được dãy đẹp, thoát khỏi vòng lặp
        if max_length == 0:
            break

        # Nếu có dãy đẹp đầu, tính độ dài để cộng vị trí
        if result["Dãy đẹp đầu"] is not None:
            length_day_dep_dau = len(result["Dãy đẹp đầu"])
        else:
            length_day_dep_dau = 0

        # Lưu dãy số đẹp tìm được vào result
        result["Dãy đẹp giữa"].append(max_sequence)
        result["Dạng đẹp giữa"].append(max_pattern_name)
        result["Vị trí giữa"].append(current_position + max_start_pos + length_day_dep_dau)

        # Thay thế dãy số đẹp bằng 'x'
        sim_number = sim_number[:max_start_pos] + 'x' * len(max_sequence) + sim_number[max_start_pos + len(max_sequence):]
        current_position = 0  # Reset vị trí về đầu để duyệt toàn bộ dãy mới
    # Tách sim_number theo dấu 'x'
    parts = sim_number.split('x')
    # Lặp qua các đoạn đã tách
    for part in parts:
        # Lặp kiểm tra cho đến khi không còn `detail` nào trong `part` nằm trong `detail_number`
        while True:
            found = False  # Biến để kiểm tra nếu tìm thấy bất kỳ `detail` nào

            # Kiểm tra từng `detail` với `part`
            for detail in detail_number:
                if detail in part:
                    # Nếu khớp, thêm vào kết quả
                    result["Dãy đẹp giữa"].append(detail)
                    result["Dạng đẹp giữa"].append("DB")
                    result["Vị trí giữa"].append(sim_number_backup.index(detail))

                    # Thay thế `detail` bằng 'x' trong `part`
                    part = part.replace(detail, 'x', 1)
                    found = True  # Đánh dấu là đã tìm thấy và thay thế

                    break  # Kiểm tra lại từ đầu `detail_number` sau khi xóa

            # Nếu không tìm thấy `detail` nào nữa, thoát khỏi vòng lặp
            if not found:
                break

    
    if len(result["Dạng đẹp giữa"]) >=2:
      result = reorder_sequences(result)
    return result

def reorder_sequences(result):
    # Kết hợp các phần tử thành danh sách các tuple
    combined = list(zip(result["Dạng đẹp giữa"], result["Dãy đẹp giữa"], result["Vị trí giữa"]))

    # Sắp xếp danh sách theo vị trí giữa
    combined.sort(key=lambda x: x[2])  # Sắp xếp theo vị trí giữa

    # Tách lại thành ba danh sách
    result["Dạng đẹp giữa"], result["Dãy đẹp giữa"], result["Vị trí giữa"] = zip(*combined)

    # Chuyển đổi từ tuple về danh sách
    result["Dạng đẹp giữa"] = list(result["Dạng đẹp giữa"])
    result["Dãy đẹp giữa"] = list(result["Dãy đẹp giữa"])
    result["Vị trí giữa"] = list(result["Vị trí giữa"])

    # Trả về kết quả sau khi sắp xếp
    return result

def count_type_number(number):
    store = set()
    count = 0
    for digit in number:
      if digit not in store:
        count += 1
        store.add(digit)
        
    return count


# #Chạy hàm với input mới
# sim_input = "0926632993"
# result = identify_beautiful_sequences_with_positions(sim_input)
# print(sim_input + ": " + str(result))
