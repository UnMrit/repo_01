import tkinter as tk
import imdb 
from bs4 import BeautifulSoup
import requests
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt 
import pandas as pd 
import lxml
import re
from PIL import Image
import numpy as np

#global variable
custom_mask = np.array(Image.open("Fb_01.jpg"))
#tag_re = ''

def create_url(id):
    """Use user entered Movie or TV Show name to generate search reviews URL in IMDb"""
    url_ = "https://www.imdb.com/title/tt" + id + "/reviews?ref_=tt_ql_3"
    return url_
    
def scrape_reviews(url_):
    """Scrape review URL to find reviews and reuturn as a list"""
    global custom_mask 
    page = requests.get(url_)
    soup = BeautifulSoup(page.content, 'lxml')
    user_review_ratings = soup.find_all('div', attrs={'class': 'text show-more__control'})
    rating =  [tag.previous_element for tag in soup.find_all('span', attrs={'class': 'point-scale'})]
    sum_ = 0

    for rat in rating:
        sum_ += float(rat)
    avg_rating = sum_/len(rating)
    
    if avg_rating >= 6.5:
        custom_mask= np.array(Image.open("Fb_01.jpg"))
    else:
        custom_mask = np.array(Image.open("Fb_02.jpg"))
    return user_review_ratings
    
def generate_wordcloud(user_review_ratings):
    """Use review text to generate a wordcloud"""
    comment_words = '' 
    stopwords = set(STOPWORDS)
    stopwords = ['movie', 'movies', 'show', 'series', 'film', 'cinema'] + list(stopwords)    
    
    for val in user_review_ratings:
        # typecaste each val to string
        tag_re = re.compile(r'<[^>]+>')
        val = str(val) 
        val = tag_re.sub('', val)
        # split the value 
        tokens = val.split() 
        # Converts each token into lowercase 
        for i in range(len(tokens)): 
            tokens[i] = tokens[i].lower() 
      
        comment_words += " ".join(tokens)+" "
        
    mask_colors = ImageColorGenerator(custom_mask)
    wordcloud = WordCloud(width = 2400, 
                          height = 2400,
                          mask=custom_mask,
                          color_func=mask_colors,
                          background_color ='white', 
                          stopwords = stopwords, 
                          min_font_size = 10).generate(comment_words) 
    
    # plot the WordCloud image                        
    plt.figure(figsize = (20, 20), facecolor = None) 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    plt.tight_layout(pad = 0) 
      
    plt.show()

    
def show_image():
    """Start the word cloud generation process"""
    ia = imdb.IMDb()
    user_in_title = e1.get()
    movie_title = ia.search_movie(user_in_title)
    url_ = create_url(movie_title[0].movieID)
    
    user_review_ratings = scrape_reviews(url_)
    generate_wordcloud(user_review_ratings)

if __name__ == "__main__":
    """Main method"""
    master = tk.Tk()
    tk.Label(master, 
             text="Name",
             activebackground='black',
             activeforeground='green',
             background='black',
             foreground='lime',
             relief='solid').grid(row=2, column=3)

    e1 = tk.Entry(master)
    e1.grid(row=2, column=4)
    
    master.configure(bg='black')
    master.geometry('290x75')
    master.title("Word Cloud Generator")
    
    tk.Button(master, 
              text='Quit', 
              command=master.quit,
              activebackground='black',
              activeforeground='green',
              background='black',
              foreground='lime',
              relief='solid').grid(row=4, 
                                   column=1, 
                                   sticky=tk.W, 
                                   pady=4)
    tk.Button(master, 
              text='Show', 
              command=show_image,
              activebackground='black',
              activeforeground='green',
              background='black',
              foreground='lime',
              relief='solid').grid(row=4, 
                                   column=5, 
                                   sticky=tk.W, 
                                   pady=4)
    
    tk.mainloop()