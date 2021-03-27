import urllib.request
from bs4 import BeautifulSoup

#get the connction between url and city_name
def get_city_url():
    city_name2url={}  # a dictionary to transfer city name to url
    url = 'http://www.weather.com.cn/forecast/'
    header = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36")  # set header
    http_handler= urllib.request.HTTPHandler()#initialize http handler
    opener = urllib.request.build_opener(http_handler)  #get opener
    opener.addheaders = [header]#initialize the header of opener
    request = urllib.request.Request(url)  #to get response
    response = opener.open(request)  # get response
    html = response.read()  # read the response
    html = html.decode('utf-8')  # decode the html as utf-8,otherwise it will be a mess

    # according to the imformation of the website code,we need to filter
    #interpreter the html by BS
    BS= BeautifulSoup(html, "html.parser")  #create  BeautifulSoup object
    body =BS.body#get html body
    sample=body.find_all('div', {'class': 'maptabboxin','style':"display: none;"})#find all the data we need
    for temp0 in sample:
        temp1=temp0.find_all('li') # search feather
        for temp2 in temp1:
            temp3=temp2.find('a')
            city_name=temp3.string #get city_name
            url=temp3.attrs['href'] #get url

            url=url.replace('1d','')#there is difference between the url we need and the url we can find,
                                    #we need to modify
            city_name2url[city_name]=url  #add city name and url to the dictionary
    return  city_name2url



#get the weather  condition :resutl,low_temperature,high_temperature,weather_condition,date
def get_weather_information(city_name,city_name2url):
    url = city_name2url[city_name]
    header = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36")  # set header
    http_handler= urllib.request.HTTPHandler()#initialize http handler
    opener = urllib.request.build_opener(http_handler)  #get opener
    opener.addheaders = [header]#initialize the header of opener
    request = urllib.request.Request(url)  #to get response
    response = opener.open(request)  # get response
    html = response.read()  # read the response
    html = html.decode('utf-8')  # decode the html as utf-8,otherwise it will be a mess

    # according to the imformation of the website code,we need to filter
    #interpreter the html by BS
    result=[]  # a list to store what we need
    BS= BeautifulSoup(html, "html.parser")  #create  BeautifulSoup object
    body =BS.body#get html body

    sample= body.find('div', {'id': '7d'})#find first sample whose name is 'div' ,attributes:id=7d
    temp1=sample.find('ul')
    data=temp1.find_all('li')#get all data


    #start to get weather infoormation
    low_temperature = []  #to store low temprature of each day
    high_temprature= []  # to store high temprature of each day
    date = []  #to store date
    weather= [] #to store weather condition
    day=0
    for each_day in data:  # get the weather data of each day
        if day < 7:
            temp = []  #to store all the infoormation of each day
            time=each_day.find('h1').string  #to get date
            temp.append(time)
            date.append(time)

            info = each_day.find_all('p')  #get the rest of infoormation

            temp.append(info[0].string)#get first piece of information _weather condition
            weather.append(info[0].string)

            low_tem= info[1].find('i').string  #the lowest temperature
            lowStr = ""
            lowStr = lowStr.join(low_tem.string)
            low_temperature.append(int(lowStr[:-1]))  # transform into int and store

            if info[1].find('span') is None:  #maybe no highest temperature
                high_tem = None
                temperature=low_tem
                high_temprature.append(int(lowStr[:-1]))#high = low
            else:
                high_tem = info[1].find('span').string  # the highest temprature
                high_tem = high_tem.replace('℃', '')
                temperature = high_tem + '/' +low_tem
                highStr = ""
                highStr = highStr.join(high_tem)
                high_temprature.append(int(highStr))  # transform into int and store

            temp.append(temperature)
            result.append(temp)
            day= day + 1
    return result,low_temperature,high_temprature,weather,date

