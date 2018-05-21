# generate word clouds
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
from django.conf import settings

def makecloud(text):
    # Generate a word cloud image
    word_list = []
    for i in text:
        word_list.append(i['genre'])
    text = " ".join(word_list)
    wordcloud = WordCloud().generate(text)
    image = wordcloud.to_image()
    img_outfile = os.path.join(settings.STATIC_ROOT,'genres.png')
    image.save(img_outfile, format='png', optimize=True)