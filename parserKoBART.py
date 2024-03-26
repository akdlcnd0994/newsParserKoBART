import torch
import requests
import re
from bs4 import BeautifulSoup
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

enterUrl = "https://m.entertain.naver.com/ranking"
newsUrl = "https://news.naver.com/section/10"
rankingUrl = "https://news.naver.com/main/ranking/popularDay.naver"

def short(text):
    tokenizer = PreTrainedTokenizerFast.from_pretrained('digit82/kobart-summarization')
    model = BartForConditionalGeneration.from_pretrained('digit82/kobart-summarization')

    text = text.replace('\n', ' ')

    raw_input_ids = tokenizer.encode(text)
    input_ids = [tokenizer.bos_token_id] + raw_input_ids + [tokenizer.eos_token_id]

    summary_ids = model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=1024,  eos_token_id=1)
    temp = tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)

    print(temp)

def newsParser(url, idx):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    datas = soup.find("div", {"id" : "ct_wrap"}).find_all("li", {"class" : "_SECTION_HEADLINE"})

    for data in datas:
        if(data.find("img")==None):
            continue
        else:
            img = data.find("img")["data-src"]
        link = data.find("div",{"class":"sa_text"}).find("a")["href"] #link
        title= data.find("strong",{"class":"sa_text_strong"}).get_text() + " - " + data.find("div",{"class":"sa_text_press"}).get_text() #title

        r2 = requests.get(link)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        text = soup2.find("div", {"id" : "ct_wrap"}).find("article", {"id" : "dic_area"}).get_text()


        text = re.sub("\n", "", text) # content
        text=text[:1024]

        #koBART 호출

        short(text)

        #db - idx, title, content, link

def rankingParser(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    datas = soup.find("div", {"class" : "rankingnews_box_wrap"}).find_all("div", {"class" : "rankingnews_box"})

    for data in datas:
        img = data.find("img")["src"]
        company = data.find("strong").get_text()

        infos = data.find("ul",{"class":"rankingnews_list"}).find_all("li")
        for info in infos:
            link = info.find("a")["href"] #link
            title = info.find("a").get_text()
        
        r2 = requests.get(link)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        text = soup2.find("div", {"id" : "ct"}).find("article", {"id" : "dic_area"}).get_text()

        text = re.sub("\n", "", text) # content

        text=text[:1024]

        #koBART 호출

        short(text)

        #db - idx, title, content, link
        


def enterParser(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    datas = soup.find("div", {"id" : "ct"}).find("ul",{"class":"news_lst"}).find_all("li")

    for data in datas:
        if(data.find("div", {"class":"thumb"}).find("img")==None):
            continue
        else:
            img = data.find("div", {"class":"thumb"}).find("img")
        link = data.find("a")["href"] #url
        title= data.find("p",{"class":"tx"}).get_text() #title

        r2 = requests.get(link)
        soup2 = BeautifulSoup(r2.text, 'html.parser')
        text = soup2.find("div", {"id" : "ct_wrap"}).find("article", {"id" : "dic_area"}).get_text()

        
        text = re.sub("\n", "", text) # content
        text=text[:1024]

        #koBART 호출

        short(text)

        #db - idx = 6, title, content, link


#for i in range(0,6):
#    newsParser("https://news.naver.com/section/10" + str(i), i)
#enterParser(enterUrl)
rankingParser(rankingUrl)

