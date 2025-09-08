import time
from checkWebsite import checkWebsite
from datetime import datetime


def main():
    count = 0
    try:
        while True:
            count += 1
            now = datetime.now()
            now_str = now.strftime("%H:%M")
            print(f"[{now_str}] Checking website... Attempt #{count}")
            if checkWebsite():                
                time.sleep(120000000)
            else:
                print("❌ No appointments available.")
            time.sleep(60) 
    except KeyboardInterrupt:
        print("\nApp stopped by user. checked {} times.".format(count))

if __name__ == "__main__":
    main()