from bs4 import BeautifulSoup
import urllib as ur
import tkinter as tk
from tkinter.messagebox import *
import requests
import json
from PIL import ImageTk


def foursquare(city,price):
    if(price!="-"):
        response=ur.request.urlopen('https://foursquare.com/explore?mode=url&near='+city+'&price='+price+'&q=Resturant')
    else:
        response=ur.request.urlopen('https://foursquare.com/explore?mode=url&near='+city+'&q=Resturant')
    html=response.read()
    soup=BeautifulSoup(html,'html.parser')
    name=[]
    rate=[]
    add=[]
    y="""<li class="card singleRecommendation hasPhoto"""
    for link in soup.find_all('li'):
        if (y in str(link)):
            name.append(link.find('div',{"class":"venueName"}))
            if(link.find('div',{"class":"venueScore positive"})!=None):
                rate.append(link.find('div',{"class":"venueScorepositive"}))
            elif(link.find('div',{"class":"venueScoreneutral"})!=None):
                rate.append(link.find('div',{"class":"venueScoreneutral"}))
            else:
                rate.append(link.find('div',{"class":"venueScoreunknown"}))
                                                  
    rate1=[]
    for x in rate:
        if(x!=None):
            rate1.append(x.string.encode("utf-8"))
        else:
            rate1.append("?")

    ##print(rate1)

    name1=[]
    for x in name:
        name1.append(x.a.string.encode("utf-8"))
        
    name_rate=[]
    for i in range(0,len(name1)):
        name_rate.append((name1[i],rate1[i]))
    
    return name_rate


              
def yelp(city,price):
    name_rate=[]
    count=0
    while(count<30):
        if(price!="-"):
            response=ur.request.urlopen('https://www.yelp.com/search?find_desc=Restaurants&find_loc='+city+'&start='+str(count)+'&ed_attrs=RestaurantsPriceRange2.'+price)
        else:
            response=ur.request.urlopen('https://www.yelp.com/search?find_desc=Restaurants&find_loc='+city+'&start='+str(count))
            
        html=response.read()
        count+=10
        soup=BeautifulSoup(html,'html.parser')
        
        y="""<li class="regular-search-result">"""
        name=[]
        rate=[]
        name1=[]
        rate1=[]
        for link in soup.find_all('li'):
            if (y in str(link)):
                name.append(link.find('span',{"class":"indexed-bizname"}))
                rate.append(link.find('img',{"class":"offscreen"}))
        for i in name:
            name1.append(i.span.string.encode("utf-8"))
            
        for i in rate:
            try:
                s=str(i['alt'])
                rate1.append(float(s[0:3]))
            except:
                rate1.append("?")
        for i in range(0,len(name1)):
            name_rate.append((name1[i],rate1[i]))
        
    return name_rate
    


root=tk.Tk()
root.geometry("645x660")
root.configure(bg='#211C5F')
root.title("Scraping Recommender")
def locate():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    e1.delete(0,tk.END)
    city=str(lat)+" "+str(lon)
    e1.insert(tk.END,"Current Location")
    return city


def get():
    city=e1.get()
    if(city=="Current Location"):
        city=locate()
    price=e2.get()
    if city=="":
        showerror(title="Empty Field",message="Please Enter a City!")
        return
    l=["1","2","3","4","-"]
    if price not in l:
        showerror(title="Please Wait",message="Please Enter Correct Price Range!")
        return
    res1=foursquare(city,price)
    res2=yelp(city,price)
    
    counter=0
    T1.delete('1.0',tk.END)
    if(len(res1)==0):
        T1.insert(tk.END,"No results")
    for i in res1:
        counter+=1
        T1.insert(tk.END,counter)
        T1.insert(tk.END,".")
        T1.insert(tk.END,i)
        T1.insert(tk.END,"\n")
    
    #T1.config(state=tk.DISABLED)

    T2.delete('1.0',tk.END)
    if(len(res2)==0):
        T2.insert(tk.END,"No results")
        
    counter=0
    for i in res2:
        counter+=1
        T2.insert(tk.END,counter)
        T2.insert(tk.END,".")
        T2.insert(tk.END,i)
        T2.insert(tk.END,"\n")
        
    #T2.config(state=tk.DISABLED)
    for x in res1:
        for y in res2:
            if(x[0].lower()==y[0].lower()):
                print((x[0],x[1]))

w1=tk.Label(root,width=30,text="Enter City:",font=("Arial",10),bg="#d32323",fg="#FFC300")
w1.grid(row=0,column=0)

e1=tk.Entry(root,width=30,bg="#DAF7A6")
e1.grid(row =0, column =1)

#mi=ImageTk.PhotoImage(file="2.png")


b=tk.Button(root,text="Loc",command=locate)
b.grid(row=0 ,columnspan=2)
#b.config(image=mi)


l2=tk.Label(root,width=30,text="Enter price(1/2/3/4/-):",font=("Arial",10),bg="#d32323",fg="#FFC300")
l2.grid(row=1,column=0)

e2=tk.Entry(root,width=30,bg="#DAF7A6")
e2.grid(row =1, column =1)

b1=tk.Button(root,text="SUBMIT",font=("Arial",10),command=get,bg="#0c4cb2",fg="#FFC300")
b1.grid(rowspan=1,columnspan=2)

l3=tk.Label(root,width=30,text="FoursquareResults:",bg="#0c4cb2",font=("Arial",10),fg="#FFC300")
l3.grid(row=4,column=0)


T1=tk.Text(root,height=35,width=40,bg="#DAF7A6",fg="#0c4cb2")
T1.grid(row=5,column=0)

l4=tk.Label(root,width=30,text="YelpResults:",bg="#d32323",font=("Arial",10),fg="#FFC300")
l4.grid(row=4,column=1)


T2=tk.Text(root,height=35,width=40,bg="#DAF7A6",fg="#d32323")
T2.grid(row=5,column=1)
root.mainloop()