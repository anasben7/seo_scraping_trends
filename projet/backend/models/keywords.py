import pandas as pd                        
from pytrends.request import TrendReq
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def get_keywords(keyword):
    pytrend = TrendReq()
    suggest=[]
    pytrend.build_payload(kw_list=[keyword])
    related_queries = pytrend.related_queries()
    liste=list(related_queries.values())[0]
    for y in liste.values():
        n=y.values.tolist()
        suggest.append(n)
    return suggest
    

def related_topic(keyword):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword])
    related_topic=pytrend.related_topics()
    topics=[]
    liste=list(related_topic.values())[0]
    for y in liste.values():
        n=y.values.tolist()
        topics.append(n)
    return topics

def intrestByCountry(keyword):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword])
    df = pytrend.interest_by_region(resolution='COUNTRY',inc_low_vol=True)
    bf=df.reset_index().values.tolist()[0:]
    print(bf)
    return bf

def intrest_by_time(keyword,year_start=2020,year_end=2020):
    pytrend = TrendReq()
    kw_list=[keyword]
    df=pytrend.get_historical_interest(kw_list, year_start=year_start, month_start=1, day_start=1, hour_start=0, year_end=year_end, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
    bf=[df.columns.tolist()] + df.reset_index().values.tolist()
    return bf[1:]

def intrest_by_time2(keyword,year_start=2020,year_end=2020):
    pytrend = TrendReq()
    keyword=["Morocco","Khalid"]
    dict={}
    for k in keyword:
        kw_list=[k]
        df=pytrend.get_historical_interest(kw_list, year_start=year_start, month_start=1, day_start=1, hour_start=0, year_end=year_end, month_end=2, day_end=1, hour_end=0, cat=0, geo='', gprop='', sleep=0)
        bf=df.columns.tolist()[0]
        test=df.reset_index().values.tolist()[1:]
        dict[bf]=test
    return dict

def intrest_by_time3(keyword,startdate=['01','06','2020'],enddate=['27','06','2020']):
    pytrend = TrendReq()
    dataframes=[]
    kw_list=keyword
    dict={}
    year_start=int(startdate[-1])
    month_start=int(startdate[-2])
    day_start=int(startdate[-3])
    year_end=int(enddate[-1])
    month_end=int(enddate[-2])
    day_end=int(enddate[-3])
    df=pytrend.get_historical_interest(kw_list, year_start=year_start, month_start=month_start, day_start=day_start, hour_start=0, year_end=year_end, month_end=month_end, day_end=day_end, hour_end=0, cat=0, geo='', gprop='', sleep=0)
    bf=df.columns.tolist()[:-1]
    test=df.reset_index().values.tolist()[1:]
    for i in bf:
        dataframes.append(df[[i]])
    for j in dataframes:
        bf=j.columns.tolist()[0]
        test=j.reset_index().values.tolist()[1:]
        dict[bf]=test
    return dict

def related_topic2(keyword):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[keyword])
    try:
        related_topic=pytrend.related_topics()
    except pytrend.exceptions.Timeout:
        print("Timeout")
        
    bf=[]
    topics={}
    dataframes=[]
    name=[]
    dic={}
    #liste=list(related_topic.values())[0]
    for y,x in related_topic.items():
        for i,j in x.items():
            name.append(i)
            dataframes.append(j)
    
    dataframes[1].drop(columns=['hasData'],inplace=True)
    r=0
    for i in dataframes:
        dic[name[r]]=i.reset_index().values.tolist()[0:]
        r+=1
    return dic

def clustring(keyword):
    pytrend = TrendReq()
    kw_list=[keyword]
    doc=[]
    clusters=[]
    cluster=[]
    pytrend.build_payload(kw_list=[keyword])
    try:
        related_queries=pytrend.related_queries()
    except pytrend.exceptions.Timeout:
        print("WAAAAIt")

    liste=list(related_queries.values())[0]
    for y in liste.values():
        n=y.values.tolist()
        for title in n:
            doc.append(title[0])
    dic=related_topic2(keyword)
    #print(dic)
    topics=[]
    for n,x in dic.items():
        for y in x:	
            topics.append(y[5])
            topics.append(y[6])
    doc=doc+topics
    
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(doc)
    true_k = 4
    model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
    model.fit(X)
    order_centroids = model.cluster_centers_.argsort()[:, ::-1]
    terms = vectorizer.get_feature_names()
    for i in range(true_k):
        for ind in order_centroids[i, :10]:
            cluster.append(terms[ind])
        clusters.append(cluster)
        cluster=[]

    Y = vectorizer.transform([keyword])
    prediction = model.predict(Y)
    return clusters[prediction[0]]

