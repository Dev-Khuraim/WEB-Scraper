import goto
from sqlite3 import connect
import pandas

import nltk
from tkinter.ttk import *
from csv import writer
import csv
import requests
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup
# from newspaper import Article
import lxml.html as lh
import pandas as pd
from PIL import ImageTk, Image
from tkinter import *

# from urduhack.preprocessing import remove_punctuation
# from urduhack.preprocessing import remove_accents
# import matplotlib.pyplot as plt
import collections
from tkinter import *
ctg = ''
title = []
stories = []




win=Tk()

win.title('WEB SCRAPING TOOL')
win.geometry('900x500')

# win.resizable(False,False)
frame = Frame(win, width=600, height=400)
frame.pack()
frame.place(anchor='center', relx=0.5, rely=0.5)
img = PhotoImage(file="back1.png")
label = Label(frame, image = img)
label.pack()

t = True
# label.place(x=0, y=0)

def docParser(link):

    r = requests.get(link)
    content = r.content
    return BeautifulSoup(content, 'html.parser')

def Scrap(Web):

    with open('scraping.csv', 'w',encoding='utf-8', newline='') as f:
        fieldnames = ['Title', 'Story','Category']
        thewriter = csv.DictWriter(f, fieldnames =fieldnames)

        thewriter.writeheader()

        soup = docParser(Web)

        categories = soup.find_all('a', class_='bbc-puhg0e e1ibkbh73')
        for category_links in categories:

            ctg = category_links.text
            print(ctg)
            if ctg != 'video':
                r2 = category_links.attrs['href']
            heads = linksCrawler("https://www.bbc.com"+r2)


            i = 0
            for link in heads:
                soup = docParser(link)
                heading = heading_Scrap(soup)
                i = i+1
                print(str(i)+link)
                story = story_Scrap(soup)
                print(story)
                thewriter.writerow({'Title': heading, 'Story': story, 'Category': ctg})
                if i == 100:
                    break
    t = False
# Crawls all the links and returns list of all the links of stories of specific Category
def linksCrawler(category):
    category1 = category
    count=0
    page = 1
    a = []
    while count<100:

        soup = docParser(category)
        story_Links = soup.find_all('a', class_='bbc-uk8dsi emimjbx0')


        for links in story_Links:
            a.append(links.get('href'))

        page = page+1
        category = category1+"?page="+str(page)
        count = len(a)
        print(category)
        print(count)
    return a


# Fetches Title of the Story
def heading_Scrap(soup):
    h1 = soup.find('h1').text
    return h1


# Fetches single story

def story_Scrap(soup):
        story = soup.find_all('p', class_='bbc-yabuuk e1cc2ql70')
        str1 = ''
        for st in story:
            str1 =str1+str(st.text)
        return str1
# shows unique words in the stories
def unique():
    method_labelText.set('All Unique Words In Data')
    str1 = text().split(' ')
    dict = {}
    unique_words = ''
    for r in str1:
      if dict.get(r) == None:
          dict[r] = 0
      elif r in dict:
          dict[r] = 1
    for i in dict:
        if dict[i] == 0:
            unique_words = unique_words+ i + '\n'
    return unique_words

def min_LenStory():

    df = dataFrame()
    min = len(df.iloc[0]['Value'])
    for i in range(600):
        my_str = str(df.iloc[i]["Value"])

        size = len(my_str)

        if min>size:
            rowindex = i
            min = size
    method_labelText.set('The Lengh of Minimum Story is:'+str(min))
    return rowindex

# shows the top ten words in terms of frequency
def tenwords_Frequency():
    method_labelText.set('Top Ten Words In Terms of Frequency')
    str2 = text().split(' ')
    c = collections.Counter(str2)
    mostoccur = c.most_common(10)
    data = ''

    for k, v in mostoccur:
        data = data + str(v) + ' = ' + k + '\n'

    return data
# shows the bar graph of categories with number of stories
def bar_graph():
    blogs =['Pakistan','Aas Pas','World','Sports','Entertainment','Science']
    Stories = [100,100,100,100,100,100]

# Creating a simple bar chart
    plt.bar(blogs, Stories)

    plt.title('Number Of Stories From Different Categories')
    plt.xlabel('Categories', fontsize=15)
    plt.ylabel('posts', fontsize=15)
    plt.show()


# Creating a bar chart with the parameters
    plt.bar(blogs, Stories, width=0.7, bottom=50, align='edge')

    plt.title('The Stories in Different Categories')
    plt.xlabel('Categories', fontsize=15)
    plt.ylabel('posts', fontsize=15)
    plt.show()

# returns Title of the specific row
def title(i):
    df = pd.read_excel(
        io='FetchedData.xlsx', usecols=[0], dtype={'Title': 'str'}, nrows=601, names=["Value"])
    return df.iloc[i]['Value']
# returns Story of the specific row
def story(i):
    df = pd.read_excel(
        io='FetchedData.xlsx', usecols=[1], dtype={'Story': 'str'}, nrows=601, names=["Value"])
    return df.iloc[i]['Value']
# returns Category of the specific row
def category(i):
    df = pd.read_excel(
        io='FetchedData.xlsx', usecols=[2], dtype={'Category': 'str'}, nrows=601, names=["Value"])
    return df.iloc[i]['Value']


# returns Text of  all stories
def text():


    text = ''
    df = dataFrame()
    for i in range(600):
        text = text+str(df.iloc[i]['Value'])
    newString = ""
    for i in text:
        if i.isalnum() or i.isspace():
            newString += i
    return newString



# returns dataFrame of second column
def dataFrame():

    df = pd.read_excel(
    io='FetchedData.xlsx', usecols=[1], dtype={'Story': 'str'}, nrows=601, names=["Value"])
    return df


method_labelText = StringVar()

var = StringVar()
var.set("SCRAP IT")
rowindex = 0

# returns story with maximum length
def max_LenStory():

        df = dataFrame()
        max = 0
        for i in range(600):
            my_str = str(df.iloc[i]["Value"])
            size = len(my_str)
            if max < size:
                max = size
                rowindex = i
        st = 'The Lengh of Maximum Story is:' + str(max)
        method_labelText.set(st)

        return rowindex



def tab1():

    def tab2(row):
        label_of_url.destroy()
        button_graph.destroy()
        label_of_web.destroy()
        button.destroy()
        button_Uiquewords.destroy()
        button_MAXlen.destroy()
        button_MINlen.destroy()
        button_toptenFrequency.destroy()
        entry.destroy()
        label_of_Method = Label(win, textvariable=method_labelText, bd=10, width=30, bg='yellow',
                            font=('Helvetica', 10))
        label_of_Method.grid(row=0, column=1, padx=17, pady=10)
        label_of_Title = Label(win, text='Title:', font=('Helvetica', 20))
        label_of_Title.grid(row=1, column=0)
        label_of_Title.place(x=20,y=100)
        label_of_Category = Label(win, text='Category:', font=('Helvetica', 20))
        label_of_Category.grid(row=2, column=0, padx=17, pady=10)
        label_of_Category.place(x=20,y=180)
        label_of_Story = Label(win, text='Story', font=('Helvetica', 20))
        label_of_Story.grid(row=3, column=0, padx=17, pady=10)
        label_of_Story.place(x=50,y=400)
        text_Title = Text(win, width=50, height=3, font=('hevetica', 16),bd=10)
        text_Title.grid(row=1, column=1)
        text_Title.place(x=150,y=70)
        text_Title.insert(index=INSERT, chars=title(row))
        text_Story = Text(win, width=50, height=15, font=('hevetica', 16))
        text_Story.grid(row=4, column=1)
        text_Story.place(x=150,y=270)
        text_Story.insert(index=INSERT, chars=story(rowindex))
        text_Category = Text(win, width=10, bd=10, height=2, font=('hevetica', 16))
        text_Category.grid(row=2, column=1, pady=40)
        text_Category.place(x=150,y=170)
        text_Category.insert(index=INSERT, chars=category(rowindex))
        btn_back = Button(win, text='Back',bg='blue',fg='white' ,bd=7 ,font=16,command=lambda: [delete_tab2(),tab1()])
        btn_back.grid(row=4, column=2, padx=8, pady=4)
        btn_back.place(x=800,y=400)
        def delete_tab2():
            label_of_Method.destroy()
            label_of_Title.destroy()
            label_of_Story.destroy()
            label_of_Category.destroy()
            text_Category.destroy()
            text_Story.destroy()
            text_Title.destroy()
            btn_back.destroy()

    def tab3(i):
        label_of_url.destroy()
        button_graph.destroy()
        label_of_web.destroy()
        button.destroy()
        button_Uiquewords.destroy()
        button_MAXlen.destroy()
        button_MINlen.destroy()
        button_toptenFrequency.destroy()
        entry.destroy()
        label_of_Method = Label(win, textvariable=method_labelText, bd=10, width=30, bg='yellow',
                                font=('Helvetica', 10))
        label_of_Method.grid(row=0, column=3, padx=17, pady=10)
        label_of_Title = Label(win, text='WORDS:', font=('Helvetica', 20))
        label_of_Title.grid(row=1, column=0, padx=17, pady=10)
        words = Text(win, width=10, height=20, font=('hevetica', 16))
        words.place(x=200,y=50)
        if(i == 1):
            words.insert(index=INSERT, chars=tenwords_Frequency())
        if(i==2):
            words.insert(index=INSERT, chars=unique())
        btn_back = Button(win, text='Back',bg='blue',fg='white' ,bd=7 ,font=16,command=lambda: [delete_Tab3(),tab1()])
        btn_back.place(x=800,y=400)
        def delete_Tab3():
            label_of_Method.destroy()
            label_of_Title.destroy()
            words.destroy()
            btn_back.destroy()



    label_of_web = Label(win,textvariable=var,bg='yellow',font=('Helvetica',30))
    label_of_web.place(x=350,y=0)

    url = StringVar()


    entry = Entry(win,font=9,textvariable=url,bd=7,width=40)
    entry.place(x=240,y=70)
    label_of_url = Label(win,text='Enter URL:',font=('Times New Roman',17))
    label_of_url.place(x=100,y=70)
    button = Button(win,text = 'SCRAP',fg='white',bd =5,font=('bold',10),command=lambda:[Scrap(url.get())],bg='green',width=6)
    button.place(x=620,y=70)
    button_MINlen = Button(win,text = 'Minimum Length Story',fg='white',bd =5,bg='blue',font=10, command=lambda: [tab2(min_LenStory())])
    button_MINlen.place(x=200,y=120)
    button_MAXlen = Button(win,text = 'Maximum Length Story',fg='white',bg='blue',font=10,bd =5,command=lambda: [tab2(max_LenStory())])
    button_MAXlen.place(x=400,y=120)
    button_Uiquewords = Button(win,text = 'Unique Words',bd =5,fg='white',bg='blue',font=10, command=lambda: [unique(),tab3(2)])
    button_Uiquewords.place(x=600,y=120)
    button_toptenFrequency = Button(win,text = 'Top Ten Words in Frequency',fg='white',bg='blue',bd =5,font=10,command=lambda: [tenwords_Frequency(),tab3(1)])
    button_toptenFrequency.place(x=250,y=190)
    button_graph = Button(win,text = 'Bar Graph',fg='white',bd=5,bg='blue',font=10,command=lambda:bar_graph())
    button_graph.place(x=530,y=190)
    def deletetab1():
        label_of_url.destroy()
        button_graph.destroy()
        label_of_web.destroy()
        button.destroy()
        button_Uiquewords.destroy()
        button_MAXlen.destroy()
        button_MINlen.destroy()
        button_toptenFrequency.destroy()
        entry.destroy()


tab1()





# Scrap(url.get())
win.mainloop()



