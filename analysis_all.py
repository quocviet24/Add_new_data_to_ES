from array_beauty import identify_beautiful_sequences_with_positions
import requests
import redis
import json
import requests
import time


def analysis_all_field(phone_number):
    # Khởi tạo list để lưu kết quả phân tích
    analysis = []
    
    # Tính toán các chuỗi đẹp và các phân tích khác
    result_analysis = identify_beautiful_sequences_with_positions(phone_number)

    # Khởi tạo dictionary để lưu trữ các phân tích
    analysis_dict = {
        "sl_phim": count_type_number(phone_number),
        "2_so_dau": phone_number[:2],
        "3_so_dau": phone_number[:3],
        "last_number": phone_number[-1],
        "sl_689": sum(phone_number.count(d) for d in '689'),
    }

    # Xử lý dãy đẹp đuôi
    tail_sequence = result_analysis.get("Dãy đẹp đuôi", [])
    sl_689_t = sl_04_t = 0
    if tail_sequence:
        sl_689_t = sum(tail_sequence.count(d) for d in '689')
        sl_04_t = sum(tail_sequence.count(d) for d in '04')
    
    analysis_dict["sl_689_t"] = sl_689_t
    analysis_dict["sl_04_t"] = sl_04_t

    # Tính toán các phần còn lại của số điện thoại
    remaining_phone_number_0_4 = phone_number[3:]
    phone_number_49_53 = phone_number

    # Loại bỏ các dãy đẹp từ phone_number_49_53 và remaining_phone_number_0_4
    for key in ["Dãy đẹp đầu", "Dãy đẹp giữa", "Dãy đẹp đuôi"]:
        if result_analysis.get(key):
            values = result_analysis[key] if isinstance(result_analysis[key], list) else [result_analysis[key]]
            for value in values:
                phone_number_49_53 = phone_number_49_53.replace(value, "")
                remaining_phone_number_0_4 = remaining_phone_number_0_4.replace(value, "")

    # Tính các trường còn lại trong phân tích
    analysis_dict["sl_49_53_not_in"] = phone_number_49_53.count('49') + phone_number_49_53.count('53')
    analysis_dict["sl_0_4_not_in"] = remaining_phone_number_0_4.count('0') + remaining_phone_number_0_4.count('4')
    analysis_dict["sl_dep_lien_duoi"] = calculate_tail_length(result_analysis)
    analysis_dict["len_incre_or_decre__tail"] = len_incre_or_decre__tail(phone_number)
    
    # Xử lý trường khen hiếm
    if result_analysis.get("Dãy đẹp đuôi"):  # Kiểm tra xem có tail hay không
        if result_analysis.get("Dãy đẹp đầu"):  # Có cả head và tail
            tail_count, head_tail_count = process_tail_and_head(result_analysis)
            analysis_dict["khan_hiem_tail"] = tail_count
            analysis_dict["khan_hiem_head_and_tail"] = head_tail_count
        else:  # Chỉ có tail, không có head
            analysis_dict["khan_hiem_tail"] = process_tail(result_analysis)
            analysis_dict["khan_hiem_head_and_tail"] = 0
    else:  # Không có tail
        analysis_dict["khan_hiem_tail"] = 0
        analysis_dict["khan_hiem_head_and_tail"] = 0


    # Kết hợp các phân tích trong result_analysis vào analysis_dict
    combined_analysis = {**analysis_dict, **result_analysis}

    # Thêm kết quả phân tích vào danh sách
    analysis.append(combined_analysis)

    return analysis

# Kết nối Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# Hết hạn 1 ngày (86400 giây)
CACHE_EXPIRATION_TIME = 86400*7  

def get_cached_data(key):
    """
    Lấy dữ liệu từ cache Redis.
    Nếu không tìm thấy, trả về None.
    """
    data = redis_client.get(key)
    if data:
        return json.loads(data)  # Chuyển đổi dữ liệu JSON từ Redis
    return None

def set_cached_data(key, data):
    """
    Lưu dữ liệu vào Redis.
    Dữ liệu sẽ hết hạn sau 1 ngày.
    """
    redis_client.setex(key, CACHE_EXPIRATION_TIME, json.dumps(data))  # Lưu với thời gian hết hạn là 1 ngày

def count_documents_tail(tail_value):
    """
    Kiểm tra Redis trước khi gọi API để xem có dữ liệu chưa.
    Nếu có, lấy từ Redis, nếu không thì gọi API và lưu vào Redis.
    """
    cache_key = f"tail_count:{tail_value}"  # Key cho tail trong cache
    cached_data = get_cached_data(cache_key)
    
    if cached_data:
        return cached_data  # Trả lại dữ liệu từ cache nếu có
    
    # Nếu không có dữ liệu trong cache, gọi API
    url = f"https://dev-api.sim.vn/search4/query4/?tail={tail_value}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()  # Chuyển đổi phản hồi thành JSON
        total = data.get("meta", {}).get("total", 0)
        
        # Lưu vào Redis để sử dụng lần sau
        set_cached_data(cache_key, total)
        
        return total
    except requests.RequestException as e:
        print(f"API Request failed: {e}")
        return 0

def count_documents_tail_and_head(tail_value, head_value):
    """
    Kiểm tra Redis trước khi gọi API để xem có dữ liệu chưa.
    Nếu có, lấy từ Redis, nếu không thì gọi API và lưu vào Redis.
    """
    cache_key = f"head_tail_count:{tail_value}_{head_value}"  # Key cho head_tail trong cache
    cached_data = get_cached_data(cache_key)
    
    if cached_data:
        return cached_data  # Trả lại dữ liệu từ cache nếu có
    
    # Nếu không có dữ liệu trong cache, gọi API
    url = f"https://dev-api.sim.vn/search4/query4/?tail={tail_value}&head={head_value}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        data = response.json()  # Chuyển đổi phản hồi thành JSON
        total = data.get("meta", {}).get("total", 0)
        
        # Lưu vào Redis để sử dụng lần sau
        set_cached_data(cache_key, total)
        
        return total
    except requests.RequestException as e:
        print(f"API Request failed: {e}")
        return 0

def process_tail_and_head(result_analysis):
    tail_value = result_analysis.get("Dãy đẹp đuôi")
    head_value = result_analysis.get("Dãy đẹp đầu")

    if not tail_value:
        return 0, 0  # Không có tail, không cần gọi API

    # Kiểm tra và lấy dữ liệu từ Redis hoặc gọi API nếu không có
    tail_count = count_documents_tail(tail_value)
    head_tail_count = count_documents_tail_and_head(tail_value, head_value)

    return tail_count, head_tail_count

def process_tail(result_analysis):
    tail_value = result_analysis.get("Dãy đẹp đuôi")

    if not tail_value:
        return 0, 0  # Không có tail, không cần gọi API

    # Kiểm tra và lấy dữ liệu từ Redis hoặc gọi API nếu không có
    tail_count = count_documents_tail(tail_value)

    return tail_count

def count_type_number(number):
    return len(set(number))
  
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
    length_incre = length_decre = 1

    for i in range(len(number)-1, 0, -1):
        if number[i] >= number[i-1]:
            length_incre += 1
        if number[i] <= number[i-1]:
            length_decre += 1
    
    return max(length_incre, length_decre)
