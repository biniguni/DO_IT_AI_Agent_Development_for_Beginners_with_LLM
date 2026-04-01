from datetime import datetime

def get_current_time():
    now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now_date)
    return now_date

if __name__ == '__main__':
    get_current_time()