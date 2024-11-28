from elasticsearch import Elasticsearch
import logging


# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# # Kết nối tới Elasticsearch
elastic_local = Elasticsearch(
    [{"host": "103.143.142.224", "port": 9200, "scheme": "http"}],
    request_timeout=160  # Thay đổi giá trị này theo yêu cầu
)


def count_records_with_sl_phim(elastic_client, index_name):
    # Truy vấn Elasticsearch để đếm số lượng bản ghi có trường sl_phim tồn tại
    query = {
        "query": {
            "bool": {
                "filter": {
                    "range": {
                        "sl_0_4_7not_in": {
                            "lt": 0
                        }
                    }
                }
            }
        }
    }

    # Thực hiện truy vấn và lấy tổng số lượng kết quả
    response = elastic_client.count(
        index=index_name,
        body=query
    )
    
    # Trả về số lượng bản ghi có trường sl_phim tồn tại
    return response['count']

def count_records_with_sl_phim_2(elastic_client, index_name):
    # Truy vấn Elasticsearch để đếm số lượng bản ghi có trường sl_phim tồn tại
    query = {
        "query": {
            "range": {
                "p": {
                    "lt": 500000  # Điều kiện p < 500000
                }
            }
        }
    }

    # Thực hiện truy vấn và lấy tổng số lượng kết quả
    response = elastic_client.count(
        index=index_name,
        body=query
    )
    
    # Trả về số lượng bản ghi có trường sl_phim tồn tại
    return response['count']

# Ví dụ gọi hàm
count = count_records_with_sl_phim_2(elastic_local, 'khoso')
print(f"Số lượng bản ghi có trường 'p' < 500000: {count}") 
  
count = count_records_with_sl_phim(elastic_local, 'khoso')
print(f"Số lượng bản ghi có trường 'sl_0_4_7not_in < 0: {count}")