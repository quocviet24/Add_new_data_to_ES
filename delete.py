from elasticsearch import Elasticsearch, helpers
import logging

# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Kết nối tới Elasticsearch
elastic_local = Elasticsearch(
    [{"host": "103.143.142.224", "port": 9200, "scheme": "http"}],
    request_timeout=160  # Thay đổi giá trị này theo yêu cầu
)

def delete_field_from_index(index_name, field_name):
    try:
        # Tạo query tìm tất cả tài liệu
        query = {
            "query": {
                "match_all": {}
            }
        }

        # Sử dụng scan để lấy tất cả tài liệu theo từng batch
        actions = []
        for doc in helpers.scan(elastic_local, index=index_name, query=query, scroll='5m', size=1000):
            doc_id = doc['_id']
            
            # Cập nhật tài liệu để xóa trường
            update_action = {
                "_op_type": "update",
                "_index": index_name,
                "_id": doc_id,
                "script": {
                    "source": f"if (ctx._source.containsKey('{field_name}')) {{ ctx._source.remove('{field_name}') }}",
                    "lang": "painless"
                }
            }

            # Thêm action vào danh sách bulk
            actions.append(update_action)

            # Nếu batch đầy, thực hiện bulk update
            if len(actions) >= 1000:
                helpers.bulk(elastic_local, actions)
                actions = []  # Reset lại danh sách actions

        # Nếu còn lại các action chưa được gửi, thực hiện bulk update lần cuối
        if actions:
            helpers.bulk(elastic_local, actions)
        
        logger.info(f"Đã xóa trường '{field_name}' từ tất cả tài liệu trong index '{index_name}'")
    except Exception as e:
        logger.error(f"Lỗi khi xóa trường '{field_name}' từ index '{index_name}': {e}")

# Gọi hàm để xóa trường khan_hiem_head_and_tail
delete_field_from_index("khoso", "khan_hiem_head_and_tail")
