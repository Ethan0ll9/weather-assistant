import requests
import json

def get_data():

    # 中央氣象局台北市 api
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    parameters = {
        "Authorization" : "CWA-DC885251-6E8F-4B11-A21F-1F485D99EA13",
        "locationName" : "臺北市"
    }

    r = requests.get(url, params = parameters)
    #result = r.json()
    #print(result)
    print(r.status_code)

    if r.status_code == 200:
        
        data = json.loads(r.text)

        location = data["records"]["location"][0]["locationName"]
        weatherElement = data["records"]["location"][0]["weatherElement"]
        start_time = weatherElement[0]["time"][0]["startTime"]
        end_time = weatherElement[0]["time"][0]["endTime"]
        weather_status = weatherElement[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weatherElement[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weatherElement[2]["time"][0]["parameter"]["parameterName"]
        con = weatherElement[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weatherElement[4]["time"][0]["parameter"]["parameterName"]

        # weather_data = [location, start_time, end_time, weather_status, rain_prob, min_tem, con, max_tem]
        # for i in weather_data:
        #     print(i)
        
        # 資料打包成 tuple ，不過要記住索引值
        line_notify(tuple([location, start_time, end_time, weather_status, rain_prob, min_tem, con, max_tem]))

    else:
        print("Can't get data")
        line_notify(tuple()) # 有可能沒資料

def line_notify(data):

    token = "UpN6oUxoHi8fOqmIAewqWtORIT8BWAYGtDtMUPnfABc" #1 on 1
    #token = "Aeij5pKP8BGYkDIjwmhLxTVXocZlQ1Y2y8K0oh0c2X0" # group with mental
    message = ""

    if len(data) == 0:
        message += "\n[Error]無法取得資料"
    else:
        message += f"\n今天{data[0]}天氣：{data[3]}\n"
        message += f"溫度：{data[5]}°C - {data[7]}°C\n"
        message += f"降雨機率：{data[4]}%\n"
        message += f"體感：{data[6]}\n"
        message += f"時間{data[1]} - {data[2]}"
        if int(data[7]) >= 33:
            message += "\n超熱，會熱死！"
        if int(data[5]) <= 10:
            message += "\n要凍僵了..."
        elif int(data[5]) <= 14:
            message += "\n超冷，出門要包的跟木乃伊一樣！！！"
        elif int(data[5]) <= 19:
            message += "\n涼涼的，加件外套吧！"
        if int(data[4]) >= 70:
            message += "\n會下雨，記得帶傘！"

    # line notidy 所需資料
    url = "https://notify-api.line.me/api/notify"
    line_headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization" : "Bearer " + token
    }
    line_data = {
        "message" : message
    }
    
    requests.post(url, headers=line_headers, data=line_data)

if __name__ == "__main__":
    #line_notify(tuple(["臺北市", "2023-11-19 00:00:00", "2023-11-19 06:00:00", "晴時多雲", 60, 15, "寒冷", 33]))
    get_data()
    
