from elasticsearch import Elasticsearch
import concurrent.futures
from elasticsearch.helpers import bulk
import logging
from analysis_all import analysis_all_field
import time


# Thiết lập logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# # Kết nối tới Elasticsearch
# elastic = Elasticsearch(
#     [{"host": "103.143.142.224", "port": 9200, "scheme": "http"}],
#     request_timeout=160  # Thay đổi giá trị này theo yêu cầu
# )

elastic_local = Elasticsearch(
    ["http://localhost:9200"],
    basic_auth=('root', '123456'),
    request_timeout=160  # Thay đổi giá trị này theo yêu cầu
)

def process_batch(hits):
    actions = []
    for item in hits:
        phone_number = item.get('_id')

        if phone_number and len(phone_number) == 10:
            try:
                # Tính toán các trường mới
                analysis_results = analysis_all_field(phone_number)
                
                if analysis_results:
                    new_record = {
                        "sl_phim": analysis_results[0].get("sl_phim"),
                        "2_so_dau": analysis_results[0].get("2_so_dau"),
                        "3_so_dau": analysis_results[0].get("3_so_dau"),
                        "last_number": analysis_results[0].get("last_number"),
                        "sl_689": analysis_results[0].get("sl_689"),
                        "sl_689_t": analysis_results[0].get("sl_689_t"),
                        "sl_04_t": analysis_results[0].get("sl_04_t"),
                        "sl_49_53_not_in": analysis_results[0].get("sl_49_53_not_in"),
                        "sl_0_4_not_in": analysis_results[0].get("sl_0_4_not_in"),
                        "sl_dep_lien_duoi": analysis_results[0].get("sl_dep_lien_duoi"),
                        "len_incre_or_decre__tail": analysis_results[0].get("len_incre_or_decre__tail"),
                        "khan_hiem_tail": analysis_results[0].get("khan_hiem_tail"),
                        "khan_hiem_head_and_tail": analysis_results[0].get("khan_hiem_head_and_tail"),
                        "Dạng đẹp đầu": analysis_results[0].get("Dạng đẹp đầu"),
                        "Dãy đẹp đầu": analysis_results[0].get("Dãy đẹp đầu"),
                        "Vị trí đầu": analysis_results[0].get("Vị trí đầu"),
                        "Dạng đẹp giữa": analysis_results[0].get("Dạng đẹp giữa"),
                        "Dãy đẹp giữa": analysis_results[0].get("Dãy đẹp giữa"),
                        "Vị trí giữa": analysis_results[0].get("Vị trí giữa"),
                        "Dạng đẹp đuôi": analysis_results[0].get("Dạng đẹp đuôi"),
                        "Dãy đẹp đuôi": analysis_results[0].get("Dãy đẹp đuôi"),
                        "Vị trí đuôi": analysis_results[0].get("Vị trí đuôi")
                    }

                    actions.append({
                        "_op_type": "update",  # Sử dụng update để giữ nguyên các trường cũ
                        "_index": 'sim_number',
                        "_id": phone_number,
                        "doc": new_record  # Chỉ cập nhật các trường mới
                    })
            except Exception as e:
                logger.error(f"Error processing phone number {phone_number}: {e}")
                continue  # Bỏ qua nếu có lỗi trong tính toán

        else:
            logger.warning(f"Invalid or missing phone number for document: {item['_id']}")

    return actions

def fetch_and_handle_data_pro_ver2():
    limit = 9000  # Limit documents fetched at once
    scroll_time = '10m'  # Scroll context time

    while True:
        # Lấy dữ liệu từ Elasticsearch
        initial_response = elastic_local.search(
            index="sim_number",
            body={
                "query": {
                    "term": {
                        "m": 10
                    }
                },
                "size": limit
            },
            scroll=scroll_time
        )

        scroll_id = initial_response['_scroll_id']
        hits = initial_response['hits']['hits']

        if not hits:
            print("No more documents to process.")
            break

        while hits:
            # Chia các hits thành các batch nhỏ hơn
            batches = [hits[i:i + 1000] for i in range(0, len(hits), 1000)]
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=24) as executor:
                results = list(executor.map(process_batch, batches))

            all_actions = []
            for actions in results:
                all_actions.extend(actions)

            if all_actions:
                try:
                    start_time = time.time()

                    # Tăng tốc độ bằng cách batch size nhỏ hơn (có thể là 500 hoặc 1000)
                    bulk(elastic_local, all_actions, chunk_size=1000)

                    elapsed_time = time.time() - start_time
                    logger.info(f"Indexed {len(all_actions)} documents successfully in {elapsed_time:.2f} seconds.")

                except Exception as e:
                    logger.error(f"Error indexing documents: {e}")

            try:
                # Lấy thêm dữ liệu từ Elasticsearch với scroll
                initial_response = elastic_local.scroll(scroll_id=scroll_id, scroll=scroll_time)
                scroll_id = initial_response['_scroll_id']
                hits = initial_response['hits']['hits']
            except Exception as e:
                logger.error(f"Error while fetching scroll data: {e}")
                break

    # Clear scroll context khi hoàn thành
    elastic_local.clear_scroll(scroll_id=scroll_id)
    
fetch_and_handle_data_pro_ver2()