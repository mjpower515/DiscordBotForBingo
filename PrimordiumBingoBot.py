import discord
import os
import math
from PIL import Image, ImageDraw, ImageFont
import random

#Theme Variables as Global

themes = {'Default': {'fill_color': (255,255,255, 125),
                      'outline_color': (0, 0, 0, 255),
                      'font_color': (0,0,0,255),
                      'BackgroundImage': 'BGI2.png',
                      'X_color': (255,0,0,125),
                      'font_name': 'verdana',
                      }
          }


def get_theme(theme_name = 'Default'):
    ''' uses theme dictionary to assign global variables to specified theme'''
    global fill_color, outline_color, font_color, background_image, X_color, font_name
    fill_color = themes[theme_name]['fill_color']
    outline_color = themes[theme_name]['outline_color']
    font_color = themes[theme_name]['font_color']
    background_image = themes[theme_name]['BackgroundImage']
    X_color = themes[theme_name]['X_color']
    font_name = themes[theme_name]['font_name']

def read_options(list_name = 'BingoList.txt'):
    ''' loads in posible squares from local list
        optional filename as input'''
    options = {'free spaces':[],
               'other options':[]}
    with open(list_name,'r') as f:
        for l in f.readlines():
            if 'FREE SPACE:' in l.upper():
                tmp = l.split(':')[1].strip()
                options['free spaces'].append(tmp)
            else:
                options['other options'].append(l.strip())
    return options
    
    
    
def drawBoard(squares=[]):
    im = Image.open(background_image).convert("RGBA")
    w, h = im.size
    buf_perc = .03 # consider theme option
    buf_pix = 2*buf_perc*w
    font_buf = 10 # consider theme option (pixels)
    border_size = 3 # consider theme option (pixels)
    square_size = int((w -buf_pix)/5)
    buf_pix = (w - square_size*5)/2
    sqrs = Image.new("RGBA", im.size, (255,255,255,0)) #new imnage used for later alpha composite
    draw = ImageDraw.Draw(sqrs)
    word = 0
    strings = []
    font_range = square_size - font_buf*2
    for i in range(0,5):
        for j in range(0, 5,):
            x = buf_pix+square_size*i
            y = h - (buf_pix+square_size*j)
            
            draw.rectangle([(x,y-square_size),(x+square_size,y)], fill = fill_color,
                        outline = outline_color, width = border_size)
            f = get_font(squares[word], font_range)
            t = add_linebreaks(f, squares[word],font_range)
            l, top, r, bottom = f.getbbox(t)
            f_x = x+square_size/2
            f_y = y-square_size/2
            draw.multiline_text((f_x,f_y),t, fill=font_color, font = f, anchor = 'mm', align='center')
            word+=1
            strings.append(t)
    draw.rectangle([(buf_pix-border_size, h-(buf_pix+square_size*5)-border_size),(buf_pix+square_size*5+border_size,h - (buf_pix)-border_size)],
                   outline = outline_color, width = border_size)
    
    out = Image.alpha_composite(im,sqrs)
    return out
def get_longest_word(s):
    wc = s.count(' ')+1
    if wc >1:
        wl = 0
        for word in s.split(' '):
            if len(word)>wl:
                wl = len(word)
                longest_word = word
    else:
        longest_word = s
    return longest_word
    
def get_font(string, test_size):
    max_font = 40
    min_font = 0
    size = max_font//2
    longest_word = get_longest_word(string)

    while max_font-min_font > 1:
        font = ImageFont.truetype(font=font_name,size=size)
        left, top, right, bottom = font.getbbox(string)
        l, t, r, b = font.getbbox(longest_word)
        ww = r-l
        h = bottom-top
        w = right-left
        if h*w/test_size >= test_size or ww >= test_size:
            max_font = size
        elif h*w/test_size < test_size:
            min_font = size
        else:
            break
        size = min_font + (max_font - min_font)//2
    size = min_font
    font = ImageFont.truetype(font=font_name,size=size)
    return font

def add_linebreaks(font, string, test_size):
    left, top, right, bottom = font.getbbox(string)
    longest_word = get_longest_word(string)
    l, t, r, b = font.getbbox(longest_word)
    ww = r-l
    h = bottom-top
    w = right-left
    line_start = 0
    i=0
    out_string = ''
    while i < len(string) and i>-1:# and z < len(string):
        tmp = string.find(' ', i+1)
        if tmp != -1:
            sub = string[line_start:tmp]
            l, t, r, b = font.getbbox(sub)
            if r-l > test_size:
                out_string += string[line_start:i]+'\n'
                line_start = i+1
            
        elif i==0:
            break
        else:
            out_string += string[len(out_string):i]+'\n'
        i=tmp
            
    out_string += string[len(out_string):]

    return out_string
    
    

def new_board():
    spaces = read_options()
    get_theme()
    sqs = random.sample(spaces['other options'], k=24)
    sqs.insert(12,random.choice(spaces['free spaces']))
    board = drawBoard(squares=sqs)
    board.show()
    
    


new_board()
    
    
