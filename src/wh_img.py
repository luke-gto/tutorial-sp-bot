from whapi import search
from whapi import get_id, random_article, return_details
import random
import requests
import time
import io
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

api = 'https://www.wikihow.com/api.php?format=json&action='

def resize(im):
    image = Image.open(im)
    resized_image = image.resize((800, 600))
    return resized_image

def resize_title(string):
    if len(string) > 0:
        title = string
        text = title
        n = 42
        words = iter(text.split())
        lines, current = [], next(words)
        for word in words:
            if len(current) + 1 + len(word) > n:
                lines.append(current + ' \n')
                current = word
            else:
                current += ' ' + word
        lines.append(current)
        titleok = '\n'.join(lines)
        return titleok


def random_title():
    random_howto = random_article() #returns an ID

    article_info = return_details(random_howto) #gets the info in a dict

    return resize_title('How to ' + (article_info['title']))

def custom_title(title_input):
    if len(title_input) == 0:        
        titleok = 'No title provided by the user'
        return titleok
    
    if len(title_input) > 0:
        return resize_title(title_input)


def title_from_keyword(keyword):

    search_results = search(keyword, 5)
    if len(search_results) == 0:        
        
        return -1
    
    if len(search_results) > 0:
        return resize_title("How To " + search_results[random.randrange(0, len(search_results))]['title'])

def get_images(id):
    
    images = []
    r = requests.get(api + 'parse&prop=images&pageid=' + str(id))
    data = r.json()
    image_list = data['parse']['images']
    if not image_list:
        return 2
    else:
        for i in image_list:
            im_data = requests.get(api + 'query&titles=File:' + i + '&prop=imageinfo&iiprop=url')
            image_info = im_data.json()
            pages = image_info['query']['pages']
            for key in pages.keys():
                image_url = pages[key]['imageinfo'][0]['url']
                if image_url != 'https://www.wikihow.com/images/7/78/Incomplete_856.gif':
                    images.append(image_url)
                    return images
                
def get_images_list():
    imlistio = []
    image_link_list = []
    i = 1
    while (i < 5):
        images = []                
        image_link_list = get_images(random_article())
        
        if type(image_link_list) == list:
            images.append(image_link_list[random.randrange(0, len(image_link_list))])
            single_image_link = images[random.randrange(0, len(images))]
            response = requests.get(single_image_link)
            img_content = io.BytesIO(response.content)
            imlistio.append(img_content)    #imgs to be resized
            time.sleep(1)
            i = i + 1
        if type(image_link_list) != list:
            print("error handling")
            i  = abs(i - 1)
            
    return imlistio

def print_tutorial(titleok):

    listresized = list(map(resize, get_images_list()))    

    back = Image.new('RGBA', (1620, 1520), 'white')
    back_im = back.copy()
    back_im.paste(listresized[0], (5, 300))
    back_im.paste(listresized[1], (815, 300))
    back_im.paste(listresized[2], (5, 915))
    back_im.paste(listresized[3], (815, 915))

    draw = ImageDraw.Draw(back_im)
    font = ImageFont.truetype('Roboto-Regular.ttf', 80)

    draw.text((5, 20), titleok,(0,0,0),font=font, spacing=0)

    bio = BytesIO()    
    back_im.save(bio, format='PNG')
    io_image = bio.getvalue()

    return io_image
