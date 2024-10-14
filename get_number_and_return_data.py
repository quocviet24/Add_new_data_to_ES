from analysis_all import analysis_all_field
from elasticsearch import Elasticsearch

# kết nối tới Elasticsearch 
elastic = Elasticsearch([{"host":"178.128.19.94","port":9200,"scheme": "http"}])
elastic_stl = Elasticsearch([{"host":"103.143.142.224","port":9200,"scheme": "http"}])

# elastic_local = Elasticsearch(
#     ["http://localhost:9200"],
#     http_auth=('root', '123456') 
# )

def get_data():
    try:
        # Lấy dữ liệu từ Elasticsearch server
        response = elastic_stl.search(
            index="khostk",  
            body={
                "query": {"match_all": {}},  # Lấy tất cả dữ liệu
                "size": 10  # Lấy 50 tài liệu để phân tích
            }
        )

        # Kiểm tra kết quả trả về
        hits = response['hits']['hits']
        return hits
    except Exception as e:
      print(f"Lỗi xảy ra: {e}")

def handle_and_push_data(hits):
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
              index="kho_so",  
              id=doc_id,  
              body=updated_doc  # Cập nhật dữ liệu với kết quả phân tích mới
          )
          
          print(f"Đã cập nhật tài liệu với ID {doc_id}: {result['result']}")
      
      print("Đã hoàn thành cập nhật các tài liệu!")


hits = get_data()
handle_and_push_data(hits)
