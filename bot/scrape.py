
import requests
from datetime import datetime as dt
from lxml import html

def stringify(listt):
	return " ".join(listt).strip()

import psycopg2



r = requests.get('http://new.theastrologer.com/daily-horoscope/')
a = html.fromstring(r.text)
date = a.xpath('//body//div[@class="tab-content daily-horoscope-tabs-mobile"]//div[@id="today"]/div[@class="daily-horoscope-date-mobile"]/text()')
date_str = "".join(date)
datetime_obj = dt.strptime(date_str, "%b %d, %Y")
overview = a.xpath('//body//div[@class="tab-content daily-horoscope-tabs-mobile"]//div[@id="today"]/div[@class="shareable-section-wrapper shareable-overview"]//text()')
overview_text = stringify(overview)
all_data = a.xpath('//body//div[@class="tab-content daily-horoscope-tabs-mobile"]//div[@id="today"]/div[@class="shareable-section-wrapper"]/div')
results = {}
# results['overview'] =  overview_text
# results['date'] = datetime_obj

for each_horoscope in all_data:
 	sign_name = stringify(each_horoscope.xpath('./h2[1]/text()'))
 	sign_horoscope = stringify(each_horoscope.xpath('./text()'))
 	results[sign_name] = sign_horoscope



conn = psycopg2.connect(database="dchoduoa3bq38c", user="gvlmsvmkedkctk", password="wLO8EulDLu0uM2JLTz6dAXePmE", host="ec2-54-225-111-9.compute-1.amazonaws.com", port="5432")
cur = conn.cursor()

created_date = dt.strftime(dt.now(),"%d-%m-%Y")
overview = overview_text
horoscope_date = dt.strftime(datetime_obj, "%d-%m-%Y")

for each_horoscope in results:
	sign = each_horoscope
	horoscope = results[each_horoscope]
	query = "INSERT INTO bot_horoscope (horoscope_date, sign, horoscope, overview, created_date) VALUES (%s, %s, %s, %s, %s);" 
	data = (horoscope_date, sign, horoscope, overview, created_date)
	cur.execute(query, data)
	conn.commit()
conn.close()


date = a.xpath('//body//div[@class="tab-content daily-horoscope-tabs-mobile"]//div[@id="tomorrow"]/div[@class="daily-horoscope-date-mobile"]/text()')
date_str = "".join(date)
datetime_obj = dt.strptime(date_str, "%b %d, %Y")
overview = a.xpath('//body//div[@class="tab-content daily-horoscope-tabs-mobile"]//div[@id="tomorrow"]/div[@class="shareable-section-wrapper shareable-overview"]//text()')
overview_text = stringify(overview)
all_data = a.xpath('//body//div[@class="tab-content daily-horoscope-tabs-mobile"]//div[@id="tomorrow"]/div[@class="shareable-section-wrapper"]/div')
results = {}
# results['overview'] =  overview_text
# results['date'] = datetime_obj

for each_horoscope in all_data:
 	sign_name = stringify(each_horoscope.xpath('./h2[1]/text()'))
 	sign_horoscope = stringify(each_horoscope.xpath('./text()'))
 	results[sign_name] = sign_horoscope

print len(results)


conn = psycopg2.connect(database="dchoduoa3bq38c", user="gvlmsvmkedkctk", password="wLO8EulDLu0uM2JLTz6dAXePmE", host="ec2-54-225-111-9.compute-1.amazonaws.com", port="5432")
cur = conn.cursor()

created_date = dt.strftime(dt.now(),"%d-%m-%Y")
overview = overview_text
horoscope_date = dt.strftime(datetime_obj, "%d-%m-%Y")

for each_horoscope in results:
	sign = each_horoscope
	horoscope = results[each_horoscope]
	query = "INSERT INTO bot_horoscope (horoscope_date, sign, horoscope, overview, created_date) VALUES (%s, %s, %s, %s, %s);" 
	data = (horoscope_date, sign, horoscope, overview, created_date)
	cur.execute(query, data)
	conn.commit()
conn.close()







