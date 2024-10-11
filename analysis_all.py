from array_beauty import identify_beautiful_sequences_with_positions
import requests

def analysis_all_field(phone_number):
    analysis = []
    result_analysis = identify_beautiful_sequences_with_positions(phone_number)
    
    # Khởi tạo dictionary để lưu trữ các phân tích
    analysis_dict = {
        "sl_phim": count_type_number(phone_number),
        "2_so_dau": phone_number[:2],
        "3_so_dau": phone_number[:3],
        "last_number": phone_number[-1],
        "sl_689": sum(phone_number.count(d) for d in '689'),
    }

    # Xử lý dãy đẹp đuôi nếu có
    tail_sequence = result_analysis.get("Dãy đẹp đuôi", [])
    if tail_sequence:
        analysis_dict["sl_689_t"] = sum(tail_sequence.count(d) for d in '689')
        analysis_dict["sl_04_t"] = sum(tail_sequence.count(d) for d in '04')
    else:
        analysis_dict["sl_689_t"] = 0
        analysis_dict["sl_04_t"] = 0

    # Xử lý các phần còn lại của số điện thoại
    remaining_phone_number_0_4 = phone_number[3:]
    phone_number_49_53 = phone_number

    for key in ["Dãy đẹp đầu", "Dãy đẹp giữa", "Dãy đẹp đuôi"]:
        if result_analysis.get(key):
            values = result_analysis[key] if isinstance(result_analysis[key], list) else [result_analysis[key]]
            for value in values:
                phone_number_49_53 = phone_number_49_53.replace(value, "")
                remaining_phone_number_0_4 = remaining_phone_number_0_4.replace(value, "")

    # Các trường phân tích thêm
    analysis_dict["sl_49_53_not_in"] = phone_number_49_53.count('49') + phone_number_49_53.count('53')
    analysis_dict["sl_0_4_not_in"] = remaining_phone_number_0_4.count('0') + remaining_phone_number_0_4.count('4')
    analysis_dict["sl_dep_lien_duoi"] = calculate_tail_length(result_analysis)
    analysis_dict["len_incre_or_decre__tail"] = len_incre_or_decre__tail(phone_number)
    
    if result_analysis.get("Dãy đẹp đuôi"):
        analysis_dict["khan_hiem_tail"] = count_documents_tail(result_analysis) 
        analysis_dict["khan_hiem_head_and_tail"] = count_documents_tail_and_head(result_analysis) 
    else:
        analysis_dict["khan_hiem_tail"] = 0
        analysis_dict["khan_hiem_head_and_tail"] = 0

    # Kết hợp các phân tích trong result_analysis vào analysis_dict
    combined_analysis = {**analysis_dict, **result_analysis}

    # Append combined dictionary
    analysis.append(combined_analysis)

    return analysis


def count_documents_tail(result_analysis):
    tail_value = result_analysis.get("Dãy đẹp đuôi")

    if not tail_value :
        return 0

    url = f"https://dev-api.sim.vn/search4/query4/?tail={tail_value}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()  # Chuyển đổi phản hồi thành JSON
    except requests.RequestException as e:
        print(f"API Request failed: {e}")
        data = {"error": "Không thể lấy dữ liệu từ API"}

    total = data.get("meta", {}).get("total", 0)
    return total

def count_documents_tail_and_head(result_analysis):
    tail_value = result_analysis.get("Dãy đẹp đuôi")
    head_value = result_analysis.get("Dãy đẹp đầu")

    if not tail_value or not head_value:
        return 0

    url = f"https://dev-api.sim.vn/search4/query4/?tail={tail_value}&head={head_value}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()  # Chuyển đổi phản hồi thành JSON
    except requests.RequestException as e:
        print(f"API Request failed: {e}")
        data = {"error": "Không thể lấy dữ liệu từ API"}

    total = data.get("meta", {}).get("total", 0)
    return total

import requests

def check_exit_number(number):
    url = f"https://dev-api.sim.vn/search4/query4/?in_numbers={number}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()  # Chuyển đổi phản hồi thành JSON
    except requests.RequestException as e:
        print(f"API Request failed: {e}")
        return False  # Trả về False nếu có lỗi

    # Kiểm tra nếu data không rỗng hoặc không chứa lỗi
    if not data or "error" in data:
        return False
    else:
        return True

def count_type_number(number):
    store = set()
    count = 0
    for digit in number:
      if digit not in store:
        count += 1
        store.add(digit)
        
    return count
  
  
def calculate_tail_length(result):
    # Lấy các giá trị cần thiết từ result
    tail = result["Dãy đẹp đuôi"]
    head = result["Dãy đẹp đầu"]
    middle_values = result["Dãy đẹp giữa"]
    middle_positions = result["Vị trí giữa"]
    # Nếu dãy đuôi là None hoặc rỗng, trả về 1
    if tail is None or tail == "":
        return 0
    
    if middle_values is None or middle_values == "":
        return len(tail)
    
    tail_length = len(tail)  # Độ dài của dãy đuôi
    sum_length = tail_length  # Bắt đầu với độ dài của dãy đuôi

    # Kiểm tra số lượng dãy giữa
    num_middle = len(middle_values)
    
    if num_middle == 1:
        # Nếu chỉ có 1 dãy giữa
        middle_length = len(str(middle_values[0]))
        middle_position = middle_positions[0]

        # Kiểm tra xem dãy giữa có nằm cạnh dãy đuôi không
        if middle_position + middle_length == result["Vị trí đuôi"]:
            sum_length += middle_length

    elif num_middle > 1:
        # Nếu có nhiều hơn 1 dãy giữa
        for i in range(num_middle - 1, -1, -1):  # Duyệt từ dưới lên
            middle_length = len(str(middle_values[i]))
            middle_position = middle_positions[i]

            # Kiểm tra dãy giữa thứ i có nằm cạnh dãy đuôi không
            if middle_position + middle_length == result["Vị trí đuôi"]:
                sum_length += middle_length
                break  # Dừng lại nếu đã cộng

            # Kiểm tra dãy giữa thứ i có nằm cạnh dãy giữa thứ i-1 không
            if i > 0:  # Tránh chỉ số âm
                prev_middle_length = len(str(middle_values[i - 1]))
                if middle_position + middle_length == middle_positions[i - 1] + len(str(middle_values[i - 1])):
                    sum_length += prev_middle_length
                    break  # Dừng lại nếu đã cộng

    # Kiểm tra dãy đầu
    if head:
        head_length = len(head)
        
        if num_middle > 0 and middle_positions and middle_positions[0] == head_length:
            sum_length += head_length
    return sum_length  # Trả về tổng độ dài
  
  
def len_incre_or_decre__tail(number):
  length_incre = 1
  for i in range(len(number)-1,0,-1):
      if number[i] >= number[i-1]:
          length_incre += 1
      else:
          break
      
  length_decre = 1
  for i in range(len(number)-1,0,-1):
      if number[i] <= number[i-1]:
          length_decre += 1
      else:
          break
      
  return max(length_incre, length_decre)