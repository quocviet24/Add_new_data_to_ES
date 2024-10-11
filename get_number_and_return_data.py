from analysis_all import analysis_all_field
from elasticsearch import Elasticsearch

# kết nối tới Elasticsearch
elastic = Elasticsearch([{"host":"178.128.19.94","port":9200,"scheme": "http"}])

elastic_local = Elasticsearch(
    ["http://localhost:9200"],
    http_auth=('root', '123456') 
)

def test_elasticsearch_connections():
    # Test kết nối đến cụm từ xa
    try:
        if elastic.ping():
            print("Kết nối đến Elasticsearch từ xa thành công!")
        else:
            print("Không thể kết nối đến Elasticsearch từ xa.")
    except Exception as e:
        print(f"Lỗi khi kết nối đến Elasticsearch từ xa: {e}")

    # Test kết nối đến cụm cục bộ
    try:
        if elastic_local.ping():
            print("Kết nối đến Elasticsearch cục bộ thành công!")
        else:
            print("Không thể kết nối đến Elasticsearch cục bộ.")
    except Exception as e:
        print(f"Lỗi khi kết nối đến Elasticsearch cục bộ: {e}")

def fetch_local_and_push_data_server():
    try:
        # Lấy 50 dữ liệu từ Elasticsearch cục bộ
        response = elastic_local.search(
            index="sim_number",  
            body={
                "query": {"match_all": {}},  # Lấy tất cả dữ liệu
                "size": 50  # Giới hạn lấy 50 tài liệu
            }
        )

        # Kiểm tra kết quả trả về
        hits = response['hits']['hits']
        print(f"Đã lấy được {len(hits)} tài liệu từ Elasticsearch cục bộ")

        # Đẩy từng tài liệu lên Elasticsearch từ xa
        for doc in hits:
            doc_id = doc["_id"]
            doc_body = doc["_source"]

            # Đẩy dữ liệu lên server từ xa và lưu phản hồi
            result = elastic.index(
                index="kho_so",  
                id=doc_id, 
                body=doc_body
            )

        print("Đã đẩy dữ liệu thành công lên Elasticsearch từ xa!")
    
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")


def fetch_and_analyze():
    try:
        # Lấy dữ liệu từ Elasticsearch server
        response = elastic.search(
            index="kho_so",  
            body={
                "query": {"match_all": {}},  # Lấy tất cả dữ liệu
                "size": 50  # Lấy 50 tài liệu để phân tích
            }
        )

        # Kiểm tra kết quả trả về
        hits = response['hits']['hits']
        print(f"Đã lấy được {len(hits)} tài liệu từ Elasticsearch server")

        # Lặp qua từng tài liệu, phân tích và cập nhật dữ liệu
        for doc in hits:
            doc_id = doc["_id"]  # Lấy ID của tài liệu

            # Lấy số điện thoại từ tài liệu (giả sử trường này là 'phone')
            phone_number = doc["_id"]  # Đảm bảo bạn có trường "phone" trong tài liệu
            
            if not phone_number:
                print(f"Tài liệu với ID {doc_id} không có trường 'phone'. Bỏ qua.")
                continue

            # Gọi hàm phân tích
            analysis_results = analysis_all_field(phone_number)

            # Thêm các trường từ kết quả phân tích vào body của tài liệu
            updated_doc = doc["_source"]
            updated_doc.update({
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
            })

            # Cập nhật lại tài liệu trên Elasticsearch với các trường mới
            result = elastic.index(
                index="kho_so",  # Đảm bảo bạn dùng đúng index
                id=doc_id,  # Sử dụng lại ID của tài liệu cũ
                body=updated_doc  # Cập nhật dữ liệu với kết quả phân tích mới
            )
            
            print(f"Đã cập nhật tài liệu với ID {doc_id}: {result['result']}")
        
        print("Đã hoàn thành cập nhật các tài liệu!")
    
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")



fetch_and_analyze()

# phone = "0915580369"
# results = analysis_all_field(phone)
# print(results)