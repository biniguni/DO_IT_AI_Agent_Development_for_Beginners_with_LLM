from datetime import datetime

def get_current_time():
    now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now_date)
    return now_date

tools = [
    {
        "type" : "function",
        "function" : {
            "name" : "get_current_time",
            "descriptsion" : "현재 날짜와 시간 반환",
        }
    },
]

if __name__ == '__main__':
    get_current_time()