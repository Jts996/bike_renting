import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from . import visual_method
from PIL import Image, ImageDraw, ImageFont
import cv2
#test data
original_data = pd.read_csv('train.csv')
df = original_data.loc[:6000]
df2 = original_data.loc[:10000]




def countall_year():
    df1 = pd.DataFrame(original_data.loc[5000:5500])
    df2 = original_data.loc[:8000]
    count_all1 = pd.DataFrame({'Month': np.arange(1, 13, 1), 'Count': [0] * 12})
    count_all2 = pd.DataFrame({'Month': np.arange(1, 13, 1), 'Count': [0] * 12})
    for i in range(5000,5000+df1.shape[0]):
        month = int(df1.loc[i, 'datetime'][5:7])
        count_all1.iloc[month-1, 1] += int(df1.loc[i, 'count'])
    for i in range(df2.shape[0]):
        month = int(df2.loc[i, 'datetime'][5:7])
        count_all2.iloc[month-1, 1] += int(df2.loc[i, 'count'])

    startDate1 = df1.iloc[0, 0][0:10]
    endDate1 = df1.iloc[df1.shape[0] - 1, 0][0:10]
    startDate2 = df2.iloc[0, 0][0:10]
    endDate2 = df2.iloc[df2.shape[0] - 1, 0][0:10]

    x1 = count_all1['Month']
    y1 = count_all1['Count']
    x2 = count_all2['Month']
    y2 = count_all2['Count']
    return count_all1




#stitch images methods
def catchfourpictures(image1,image2,image3,image4):

    ims = [Image.open(image1),Image.open(image2),Image.open(image3),Image.open(image4)]
    width, height = ims[0].size
    result = Image.new(ims[0].mode, (width, height * len(ims)))

    for i, im in enumerate(ims):
        result.paste(im, box=(0, i * height))

    result.save('report.jpeg')

def catchfourpictures_horizon(image1,image2,image3,image4):

    ims = [Image.open(image1),Image.open(image2),Image.open(image3),Image.open(image4)]
    width, height = ims[0].size
    result = Image.new(ims[0].mode, (2*width, height*2))
    a = True
    for i, im in enumerate(ims):
        if(a):
            result.paste(im, box=(0, int(i/2) * height))
            a = not a
        else:
            result.paste(im, box=(width, int(i/2) * height))
            a = not a
    result.save('report.jpeg')

# add blank place for add text into report(graphs)
def catchblankpictures(img):
    img = Image.open(img)
    width, height = img.size
    blankheight = 500
    newIm = Image.new('RGB', (width, blankheight), 'white')
    newIm.save(r'blank.jpeg')
    ims = [newIm,img]
    result = Image.new('RGB', (width, height+blankheight))
    result.paste(ims[0], box=(0, 0))
    result.paste(ims[1],box=(0,blankheight))
    result.save('report.jpeg')



def produceReport(period1_start='2011-01-01 01:00:00',
                            period1_end='2011-01-19 01:00:00',
                            period2_start='2011-02-05 01:00:00',
                            period2_end = '2011-02-19 01:00:00',
                            period3_start = '2011-01-02 01:00:00',
                            period3_end = '2011-03-08 01:00:00',
                            period4_start = '2011-01-02 01:00:00',
                            period4_end='2011-01-19 01:00:00',
                            period5_start='2011-02-05 01:00:00',
                            period5_end = '2011-02-19 01:00:00',
                            period6_start = '2011-01-02 01:00:00',
                            period6_end = '2011-03-08 01:00:00',
                  word="Dear manager, here is final report for you between period you choose. "):
    # 1. fisrt step draw five graphs with data from csv files or database
    # load data from dataset
    original_data = pd.read_csv('train.csv')

    df = original_data.loc[:6000]
    df2 = original_data.loc[:10000]

    visual_method.draw_count_hours(df)
    visual_method.draw_two_count_hours(df, df2)
    visual_method.draw_week_weekend_count(df)

    visual_method.draw_stack_three_week_weekend(df, period4_start, period4_end, period5_start, period5_end,period6_start, period6_end)
    visual_method.draw_stack_three_week_weekend(df, period1_start, period1_end, period2_start, period2_end, period3_start,period3_end)

    # 2. second step is to stiche four graphs we draw in first step
    image1 = 'draw_count_hours.jpeg'
    image2 = 'draw_stack_three_week_weekend.jpeg'
    image3 = 'draw_two_count_hours.jpeg'
    image4 = 'draw_three_week_weekend.jpeg'

    catchfourpictures_horizon(image1, image2, image3, image4)

    # add text to report
    header = word
    font_type = '/System/Library/Fonts/STHeiti Light.ttc'
    font_medium_type = '/System/Library/Fonts/STHeiti Medium.ttc'
    header_font = ImageFont.truetype(font_medium_type, 250)
    font = ImageFont.truetype(font_type, 24)
    color = "#000000"

    img = 'report.jpeg'

    catchblankpictures(img)

    img = 'report.jpeg'
    new_img = 'report.jpeg'
    image = Image.open(img)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    header_x = 100
    header_y = 100
    draw.text((header_x, header_y), u'%s' % header, color, header_font)

    # save report
    image.save(new_img, 'jpeg')


#test method for draw static visulation graphs
#produceReport(word = 'good day')