import os
from numpy.core.defchararray import multiply
import pandas as pd
from numpy import *
import re
from PIL import Image, ImageFont, ImageDraw

font = ImageFont.truetype('./simsun.ttc', 20)

fileNames = os.listdir('./文化理解与创新-场景三-images')


id = []

for f in fileNames:
    temp = int(f[:f.find('-')])
    id.append(temp)

dic = {}

for i in range(len(id)):
    dic[id[i]] = fileNames[i]


data = pd.DataFrame(pd.read_excel('./图片题对应的文字题.xlsx', index_col=0))


prefix = './文化理解与创新-场景三-images/'
pattern = re.compile('.{25}')
print(data.loc[id[0]])
df = pd.DataFrame(columns=['ticket_id', 'name', 'image_path'])
for i in data.index:
    if i in id:
        try:
            im = Image.open(prefix+dic[i])
            bg = Image.new('RGB', im.size, (255, 255, 255))
            bg.paste(im, (0, 0), im)
            im = bg
            draw = ImageDraw.Draw(im)
            x, y = (5, 5)
            text = data.loc[i]['text']
            if str(text) == 'nan':
                textT = "空"
            elif len(text) < 25:
                textT = text
            else:
                textT = '\n'.join(pattern.findall(text))
            draw.text((x, y), textT, font=font, fill='#000000')
            # print(dic[i][:-3]+'jpg')
            im.save('./newImages/'+str(i)+'.jpg')
            df = df.append({'ticket_id': i, 'name': data.loc[i]['name'],
                            'image_path': './newImages/'+str(i)+'.jpg'}, ignore_index=True)
        except:
            print("error")
    else:
        text = data.loc[i]['text']
        bg = Image.new('RGB', (800, 450), (255, 255, 255))
        im = bg
        text = str(text)
        if text == 'nan':
            print("error")
            textT = "空"
        elif len(text) < 25:
            textT = text
        else:
            textT = '\n'.join(pattern.findall(text))
        draw = ImageDraw.Draw(bg)
        draw.text((x, y), textT, font=font, fill='#000000')
        im.save('./newImages/'+str(i)+'.jpg')
        df = df.append({'ticket_id': i, 'name': data.loc[i]['name'],
                        'image_path': './newImages/'+str(i)+'.jpg'}, ignore_index=True)

        # im.show()
df.to_csv('./new.csv')


# for i in id:
