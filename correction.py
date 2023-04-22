import re
from enum import Enum
import random
import pandas as pd

# define categories using an Enum
class TokenCategory(Enum):
    KEYWORD = 1
    IDENTIFIER = 2
    LITERAL = 3
    OPERATOR = 4
    PUNCTUATION = 5
    COMMENT = 6
    WHITESPACE = 7

# define regular expressions for different categories
keyword_regex = re.compile(r'\b(and|as|assert|async|await|break|class|continue|def|del|elif|else|except|False|finally|for|from|global|if|import|in|is|lambda|None|nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b')
identifier_regex = re.compile(r'^[a-zA-Z_][a-zA-Z0-9_]*$')
literal_regex = re.compile(r'^(-?\d+(\.\d+)?|\'.*?\'|".*?")$')
operator_regex = re.compile(r'^(\+|\-|\*|\/|\%|\*\*|\>\>|\>\=|\<\<|\<\=|\<|\>|\=|\!\=|\&|\&&|\||\|\||\^|\~)$')
punctuation_regex = re.compile(r'^(\,|\:|\;|\(|\)|\[|\]|\{|\}|\@|\=|\->|\+=|\-=|\*=|\/=|\%=|&=|\|=|\^=|\>>=|\<\<=|\*\*=|\/\/=)$')
comment_regex = re.compile(r'^(\#.*$)')
whitespace_regex = re.compile(r'^(\s+)$')

def assign_categories_to_tokens(token_list):
    # initialize an empty list to store the categories of each token
    categories = []
    
    # iterate through each token in the list and assign its category
    for token in token_list:
        if keyword_regex.match(token):
            categories.append(TokenCategory.KEYWORD)
        elif identifier_regex.match(token):
            categories.append(TokenCategory.IDENTIFIER)
        elif literal_regex.match(token):
            categories.append(TokenCategory.LITERAL)
        elif operator_regex.match(token):
            categories.append(TokenCategory.OPERATOR)
        elif punctuation_regex.match(token):
            categories.append(TokenCategory.PUNCTUATION)
        elif comment_regex.match(token):
            categories.append(TokenCategory.COMMENT)
        elif whitespace_regex.match(token):
            categories.append(TokenCategory.WHITESPACE)
        else:
            categories.append(None) # set None for unknown category
    
    return categories

def generate_fixations_code(aois_with_tokens):

    # assign categories to each token
    categories = assign_categories_to_tokens([aoi.token for aoi in aois_with_tokens.itertuples()])
    
    fixations = []
    word_count = 0
    skip_count = 0
    regress_count = 0
    reread_count = 0
    
    index = 0
    
    print(aois_with_tokens)
    aois_with_tokens = aois_with_tokens.sample(frac = 1)
    
    while index < len(aois_with_tokens):
        aoi = aois_with_tokens.iloc[index]
        x, y, width, height, token = aoi["x"], aoi["y"], aoi["width"], aoi["height"], aoi["token"]
        category = categories[index]
        
        word_count += 1
        
        fixation_x = x + width / 3 + random.randint(-10, 10)
        fixation_y = y + height / 2 + random.randint(-10, 10)

        last_skipped = False

        # skipping
        if category in [TokenCategory.COMMENT, TokenCategory.PUNCTUATION]:
            skip_probability = 0.9
        elif category in [TokenCategory.KEYWORD, TokenCategory.OPERATOR]:
            skip_probability = 0.5
        elif category == TokenCategory.IDENTIFIER:
            skip_probability = 0.6
        else:
            skip_probability = 0.8
        
        if len(token) < 5 and random.random() < skip_probability:
            skip_count += 1
            last_skipped = True
        else:
            fixations.append([fixation_x, fixation_y, len(token) * 50])
            last_skipped = False
        
        # regression and reread
        if last_skipped:
            reread_probability = 0.01
        elif category in [TokenCategory.COMMENT, TokenCategory.PUNCTUATION]:
            reread_probability = 0.2
        elif category in [TokenCategory.KEYWORD, TokenCategory.OPERATOR]:
            reread_probability = 0.1
        elif category == TokenCategory.IDENTIFIER:
            reread_probability = 0.05
        else:
            reread_probability = 0
        
        if random.random() < reread_probability:
            reread_count += 1
        elif random.random() > 0.96:
            # between-line or previous-line regression
            i = index
            while i >= 0:
                if categories[i] == TokenCategory.PUNCTUATION or i == 0:
                    break
                i -= 1
            
            if i == index:
                index -= random.randint(1, 10)
            else:
                index = i + 1
            
            if index < 0:
                index = 0

            regress_count += 1
        
        index += 1
    
    return fixations



# write a function generate offset error as described in the paper
def error_offset(x_offset, y_offset, fixations):
    '''creates error to move fixations (shift in dissertation)'''
    
    pass


# noise
import random

def error_noise(y_noise_probability, y_noise, duration_noise, fixations):
    '''creates a random error moving a percentage of fixations '''
    
    results = []
    
    for fix in fixations:

        x, y, duration = fix[0], fix[1], fix[2]

        # should be 0.1 for %10
        duration_error = int(duration * duration_noise)

        duration += random.randint(-duration_error, duration_error)

        if duration < 0:
            duration *= -1
        
        if random.random() < y_noise_probability:
            results.append([x, y + random.randint(-y_noise, y_noise), duration])
        else:
            results.append([x, y, fix[2]])
    
    return results

# shift



# droop

from PIL import ImageFont, ImageDraw, Image
from matplotlib import pyplot as plt
import numpy as np


def draw_fixation(Image_file, fixations):
    """Private method that draws the fixation, also allow user to draw eye movement order
    Parameters
    ----------
    draw : PIL.ImageDraw.Draw
        a Draw object imposed on the image
    draw_number : bool
        whether user wants to draw the eye movement number
    """

    im = Image.open(Image_file)
    draw = ImageDraw.Draw(im, 'RGBA')

    if len(fixations[0]) == 3:
        x0, y0, duration = fixations[0]
    else:
        x0, y0 = fixations[0]

    for fixation in fixations:
        
        if len(fixations[0]) == 3:
            duration = fixation[2]
            if 5 * (duration / 100) < 5:
                r = 3
            else:
                r = 5 * (duration / 100)
        else:
            r = 8
        x = fixation[0]
        y = fixation[1]

        bound = (x - r, y - r, x + r, y + r)
        outline_color = (50, 255, 0, 0)
        fill_color = (50, 255, 0, 220)
        draw.ellipse(bound, fill=fill_color, outline=outline_color)

        bound = (x0, y0, x, y)
        line_color = (255, 155, 0, 155)
        penwidth = 2
        draw.line(bound, fill=line_color, width=5)

        x0, y0 = x, y

    plt.figure(figsize=(17, 15))
    plt.imshow(np.asarray(im), interpolation='nearest')


def draw_correction(Image_file, fixations, match_list):
    """Private method that draws the fixation, also allow user to draw eye movement order
    Parameters
    ----------
    draw : PIL.ImageDraw.Draw
        a Draw object imposed on the image
    draw_number : bool
        whether user wants to draw the eye movement number
    """

    im = Image.open(Image_file)
    draw = ImageDraw.Draw(im, 'RGBA')

    if len(fixations[0]) == 3:
        x0, y0, duration = fixations[0]
    else:
        x0, y0 = fixations[0]

    for index, fixation in enumerate(fixations):
        
        if len(fixations[0]) == 3:
            duration = fixation[2]
            if 5 * (duration / 100) < 5:
                r = 3
            else:
                 r = 5 * (duration / 100)
        else:
            r = 8

        x = fixation[0]
        y = fixation[1]

        bound = (x - r, y - r, x + r, y + r)
        outline_color = (50, 255, 0, 0)
        
        if match_list[index] == 1:
            fill_color = (50, 255, 0, 220)
        else:
            fill_color = (255, 55, 0, 220)

        draw.ellipse(bound, fill=fill_color, outline=outline_color)

        bound = (x0, y0, x, y)
        line_color = (255, 155, 0, 155)
        penwidth = 2
        draw.line(bound, fill=line_color, width=5)

        # text_bound = (x + random.randint(-10, 10), y + random.randint(-10, 10))
        # text_color = (0, 0, 0, 225)
        # font = ImageFont.truetype("arial.ttf", 20)
        # draw.text(text_bound, str(index), fill=text_color,font=font)

        x0, y0 = x, y

    plt.figure(figsize=(17, 15))
    plt.imshow(np.asarray(im), interpolation='nearest')


def find_lines_Y(aois):
    ''' returns a list of line Ys '''
    
    results = []
    
    for index, row in aois.iterrows():
        y, height = row['y'], row['height']
        
        if y + height / 2 not in results:
            results.append(y + height / 2)
            
    return results



def find_word_centers(aois):
    ''' returns a list of word centers '''
    
    results = []
    
    for index, row in aois.iterrows():
        x, y, height, width = row['x'], row['y'], row['height'], row['width']
        
        center = [int(x + width // 2), int(y + height // 2)]
        
        if center not in results:
            results.append(center)
            
    return results


def find_word_centers_and_duration(aois):
    ''' returns a list of word centers '''
    
    results = []
    
    for index, row in aois.iterrows():
        x, y, height, width, token = row['x'], row['y'], row['height'], row['width'], row['token']
        
        center = [int(x + width // 2), int(y + height // 2), len(token) * 50]

        if center not in results:
            results.append(center)
    
    #print(results)
    return results



def overlap(fix, AOI):
    """checks if fixation is within AOI"""
    
    box_x = AOI.x
    box_y = AOI.y
    box_w = AOI.width
    box_h = AOI.height

    if fix[0] >= box_x and fix[0] <= box_x + box_w \
    and fix[1] >= box_y and fix[1] <= box_y + box_h:
        return True
    
    else:
        
        return False
    
    
def correction_quality(aois, original_fixations, corrected_fixations):
    
    match = 0
    total_fixations = len(original_fixations)
    results = [0] * total_fixations
    
    for index, fix in enumerate(original_fixations):
        
        for _, row  in aois.iterrows():
            
            if overlap(fix, row) and overlap(corrected_fixations[index], row):
                match += 1
                results[index] = 1
                
    return match / total_fixations, results