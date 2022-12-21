import requests
import smtplib
import html

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY="2PG1TVVWUMUZ7EP3"
STOCK_API="https://www.alphavantage.co/query"
STOCK_API_PARAMETERS={
    "function":"TIME_SERIES_DAILY_ADJUSTED",
    "symbol":STOCK,
    "apikey":STOCK_API_KEY
}
NEWS_API_KEY="707b4f8fbc45475dbacc9b283c1c53ca"
NEWS_API="https://newsapi.org/v2/everything"
NEWS_API_PARAMERTERS={
    "apiKey":NEWS_API_KEY,
    "qInTitle":"Tesla",
}
my_mail="subhnegipython@gmail.com"
my_password="poaxujigalppestq"
recipient_mail="subhnegipython@yahoo.com"
def percentcalculator(x,y):
    return (x/y)*100
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def stockpercent():
    response=requests.get(url=STOCK_API,params=STOCK_API_PARAMETERS)
    response.raise_for_status()
    stock_data=response.json()
    stock_data=stock_data["Time Series (Daily)"]
    last_two = dict(list(stock_data.items())[:2])
    yesterday_close=list(last_two.items())[0][1]['4. close']
    day_before_yesterday_close=list(last_two.items())[1][1]['4. close']
    difference=float(yesterday_close)-float(day_before_yesterday_close)
    per=abs(percentcalculator(difference,float(day_before_yesterday_close)))
    if difference>0:
        change=f"Up{int(per)}%"
    elif difference==0:
        change="stable"
    else:
        change=f"Down:{int(per)}%"
    if per>2:
        news=get_news()
        msg=f"TSLA: {change}\n{news}"
        send_msg(msg)


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
def get_news():
    response=requests.get(url=NEWS_API,params=NEWS_API_PARAMERTERS)
    response.raise_for_status()
    response=response.json()["articles"][:3]
    news1=response[0]["title"]
    news1_des=response[0]["description"]
    news2=response[1]["title"]
    news2_des=response[1]["description"]
    news3=response[2]["title"]
    news3_des=response[2]["description"]
    news= f"Headline:{news1}\n{news1_des}\nHeadline:{news2}\n{news2_des}\nHeadline:{news3}\n{news3_des}"
    return news
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
def send_msg(msg):
    html.unescape(msg)
    with smtplib.SMTP_SSL("smtp.gmail.com") as connect:
            connect.login(user=my_mail,password=my_password)
            connect.sendmail(from_addr=my_mail,to_addrs=recipient_mail,msg=f"Subject: stock alert \n\n {msg}")

stockpercent()

#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

