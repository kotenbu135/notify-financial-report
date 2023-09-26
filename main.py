import datetime
import json

import requests

lineToken = "XXXX"
apikey = "YYYY"


def get_price(from_date, to_date):
    url = f"https://financialmodelingprep.com/api/v3/historical-price-full/SPY?from={from_date}&to={to_date}&apikey={apikey}"
    response = requests.get(url)
    data = json.loads(response.text)

    return data


def send_line_notify(notification_message):
    """
    LINEに通知する
    """
    line_notify_api = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': f'Bearer {lineToken}'}
    data = {'message': f'message: {notification_message}'}
    requests.post(line_notify_api, headers=headers, data=data)


def get_date():
    week = [-3, -4, -5, -6, 0, -1, -2]
    today = datetime.date.today()
    weekday = today.weekday()
    reduce_days = week[weekday]

    from_date = datetime.datetime.strftime(today + datetime.timedelta(reduce_days - 7), '%Y-%m-%d')
    to_date = datetime.datetime.strftime(today + datetime.timedelta(reduce_days), '%Y-%m-%d')
    return from_date, to_date


def main():
    # 前回と前々回の金曜日の日付を取得
    from_date, to_date = get_date()

    # APIを叩いて株価を取得
    data = get_price(from_date, to_date)

    # 前回と前々回の金曜日の終値を取得
    for date_data in data['historical']:
        if from_date == date_data['date']:
            from_date_close_price = date_data['close']
        if to_date == date_data['date']:
            to_date_close_price = date_data['close']

    # 下落率を計算
    weekly_rate = round(to_date_close_price / from_date_close_price * 100 - 100, 2)

    # -5%以上下げたらLINEに通知
    if weekly_rate < -5.0:
        message = (f'S&P500が１週間で {weekly_rate}% を記録しました！\n'
                   f'スポット購入のチャンスです！')
        send_line_notify(message)


if __name__ == '__main__':
    main()
