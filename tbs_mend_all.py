import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import lxml
import datetime 

index = 1

def request_tbsmend(index):
    today = datetime.date.strftime(datetime.date.today()- datetime.timedelta(days=index-1),'%Y-%m-%d')
    yesterday = datetime.date.strftime(datetime.date.today()- datetime.timedelta(days=index),'%Y-%m-%d')


    FORMURL="http://tbsnew.mand.co.kr:2189/jsp/AdminLogin.jsp"
    login_url = "http://tbsnew.mand.co.kr:2189/OperatorAction.do?cmd=login"
    stats_url = "http://tbsnew.mand.co.kr:2189/StatAction.do?cmd=statPgm&ch_key=201&start_hh=00&start_mi=00&end_hh=24&end_mi=00&start_dt={}&end_dt={}".format(yesterday,today)
    payload ={
        'oper_id':'fm_24',
        'oper_pw':'af80d34c90c2e5511dc1af7ef2e3eab1',
        'cmd':'login',
        #'Origin':'http://tbsnew.mand.co.kr:2189',
        #'X-Requested-With':'XMLHttpRequest',
        #'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }
    with requests.Session() as s:
        resp = s.get(FORMURL)
        cookies = resp.cookies
        #print(resp.cookies)
        headers = requests.utils.default_headers()
        #s.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        #login =s.post(login_url, data = payload, headers=headers, cookies=cookies)
        login =s.post(login_url, data = payload)
        #print (login.text)
        response=s.get(stats_url).text
        soup = bs(response, 'lxml')
    
        tabs = pd.DataFrame({ 
			'date':[],                        
                        'pgm_nm':[],
                         'rcv':[],
                         'tm':[],
                         'tmp1':[],
                         'new_sub':[],
                         'cur_sub':[],
                         'sum_sub':[] 
                        })
    
    for tr in soup.find_all('tr')[1:len(soup.find_all('tr'))-1]:
        #tds = tr.select('td')
        title =  tr.select('td')[0].text
        received =  tr.select('td')[1].text
        transmitted = tr.select('td')[2].text
        transmitperperson = tr.select('td')[3].text
        new_sub =  tr.select('td')[4].text
        cur_sub =  tr.select('td')[5].text
        sum_sub =  tr.select('td')[6].text

        insert_data = pd.DataFrame({
		'date':[today],
             'pgm_nm' : [title],
             'rcv' : [received],
             'tm' : [transmitted],
             'tmp1' : [transmitperperson],
             'new_sub' : [new_sub],
             'cur_sub' : [cur_sub],
             'sum_sub' : [sum_sub],
              
        })
    
        tabs =tabs.append(insert_data,sort=False)
    
    tabs.to_csv('/home/enuzeas/tbs_mend/csv_/tbsnewdemand_{}.csv'.format(today),index=False)
    print('Created tbsnewmand_{}.csv'.format(today))
for i in range(1000,2000):
	request_tbsmend(i)
  
