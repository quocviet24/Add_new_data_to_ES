import redis
import json

def display_redis_data(redis_host='localhost', redis_port=6379, redis_db=0):
    try:
        # Kết nối tới Redis
        redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

        # Liệt kê tất cả các keys trong Redis
        keys = redis_client.keys('*')  # Lấy tất cả keys

        if not keys:
            print("No keys found in Redis.")
            return

        # Duyệt qua tất cả keys và in giá trị tương ứng
        for key in keys:
            key_str = key.decode('utf-8')  # Giải mã key từ bytes sang string
            print(f"Key: {key_str}")

            # Kiểm tra loại dữ liệu của key và in ra tương ứng
            if redis_client.type(key) == b'string':
                value = redis_client.get(key)
                print(f"  Value (String): {value.decode('utf-8')}")
            elif redis_client.type(key) == b'hash':
                value = redis_client.hgetall(key)
                print("  Value (Hash):")
                for field, val in value.items():
                    print(f"    {field.decode('utf-8')}: {val.decode('utf-8')}")
            elif redis_client.type(key) == b'list':
                value = redis_client.lrange(key, 0, -1)
                print("  Value (List):")
                for item in value:
                    print(f"    {item.decode('utf-8')}")
            elif redis_client.type(key) == b'set':
                value = redis_client.smembers(key)
                print("  Value (Set):")
                for item in value:
                    print(f"    {item.decode('utf-8')}")
            elif redis_client.type(key) == b'zset':
                value = redis_client.zrange(key, 0, -1)
                print("  Value (Sorted Set):")
                for item in value:
                    print(f"    {item.decode('utf-8')}")
            else:
                print(f"  Unknown type for key: {key_str}")
            print('-' * 40)

    except Exception as e:
        print(f"Error: {e}")

# Kết nối tới Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
def count_records_in_redis():
    """
    Đếm số lượng bản ghi trong Redis bằng cách sử dụng SCAN.
    """
    count = 0
    cursor = 0

    while True:
        cursor, keys = redis_client.scan(cursor, count=1000)  # Thực hiện quét và lấy 1000 key mỗi lần
        count += len(keys)  # Cộng dồn số lượng keys tìm thấy

        if cursor == 0:
            break  # Nếu cursor = 0, quét xong tất cả các keys

    return count

#Gọi hàm để đếm số lượng bản ghi trong Redis
record_count = count_records_in_redis()
print(record_count)