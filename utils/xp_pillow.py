# Standard 
import discord
from discord.ext import commands 
from datetime import datetime, timedelta, timezone

# Third party
from PIL import Image, ImageDraw , ImageFont , ImageEnhance , ImageFilter , ImageSequence
from io import BytesIO
import requests

# Local

def level_images(member ,final_xp , lvl , rank , xp):
    background = Image.open('latte_config/images/level.png')
    
    if member.display_avatar != member.avatar:
        url = member.display_avatar.replace(format='png') #when avater gif = convert gif to png 
    elif member.avatar is not None:
        url = member.avatar.replace(format='png')
    else:
        url = member.default_avatar.replace(format='png') 
    
    response = requests.get(url)
    logo = Image.open(BytesIO(response.content)).resize((300, 300))
    whitecc =  Image.new("RGB", (310, 310), (119, 221, 119))
    bigsize = (logo.size[0] * 3, logo.size[1] * 3)
    mask = Image.new("L", bigsize, 0)

    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, 255)

    #draw.ellipse((140 * 3, 140 * 3, 189 * 3, 189 * 3), 0)

    mask = mask.resize(logo.size, Image.ANTIALIAS )
    logo.putalpha(mask)

    bigsize = (whitecc.size[0] * 3, whitecc.size[1] * 3)
    draw.ellipse((0, 0) + bigsize, 255)

    mask = mask.resize(whitecc.size, Image.ANTIALIAS )
    whitecc.putalpha(mask)

    background.paste(whitecc, (35, 45), mask=whitecc)

    background.paste(logo, (40, 50), mask=logo)

    # # Black Circle
    draw = ImageDraw.Draw(background)
    # draw.ellipse((160, 160, 208, 208), fill="#000")

    big_font = ImageFont.FreeTypeFont("latte_config/fonts/Daisy.ttf", 90)
    mid_font = ImageFont.FreeTypeFont("latte_config/fonts/Daisy.ttf", 80)
    big_2_font = ImageFont.FreeTypeFont("latte_config/fonts/Daisy.ttf", 105)
    big2_font = ImageFont.FreeTypeFont("latte_config/fonts/Daisy.ttf", 120)
    medium_font = ImageFont.FreeTypeFont("latte_config/fonts/Daisy.ttf", 70)
    small_font = ImageFont.FreeTypeFont("latte_config/fonts/Daisy.ttf", 50)

    textrank = ImageFont.FreeTypeFont("latte_config/fonts/Daisy.ttf", 130)
    ranksize = ImageFont.FreeTypeFont("latte_config/fonts/Daisy.ttf", 70)

    #level_num               
    text_size = draw.textsize(str(lvl), font=big2_font)
    offset_x = 530
    offset_y = 225
    draw.text((offset_x, offset_y), str(lvl), font=big2_font, fill="#77dd77")

    #level_text 
    text_size = draw.textsize("LEVEL", font=big_2_font)
    offset_x -= text_size[0] + 5
    levelx = 355
    levely = 220
    draw.text((levelx , levely + 15), "LEVEL", font=big_2_font, fill="#fff")

    #rank
    text_size = draw.textsize(f"#{rank}", font=textrank)
    rank_x = 1250 - 15 - text_size[0]
    rank_y = -10
    draw.text((rank_x, rank_y), f"#{rank}", font=textrank, fill="#77dd77")

    text_size = draw.textsize("RANK", font=big_2_font)
    rank_x -= text_size[0] + 5
    draw.text((rank_x, rank_y + 20), "RANK", font=big_2_font, fill="#fff")

    bar_offset_x = 370
    bar_offset_y = 340
    bar_offset_x_1 = 1250
    bar_offset_y_1 = 380
    circle_size = bar_offset_y_1 - bar_offset_y  # Diameter

    # Progress Bar
    draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#727175")

    # Left Circle
    draw.ellipse(
        (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#727175")                    

    # Right Circle
    draw.ellipse(
        (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#727175")
                    
    bar_length = bar_offset_x_1 - bar_offset_x
    progress = (final_xp - xp) * 100 / final_xp
    progress = 100 - progress
    progress_bar_length = round(bar_length * progress / 100)
    bar_offset_x_1 = bar_offset_x + progress_bar_length

    # Progress Bar
    draw.rectangle((bar_offset_x, bar_offset_y, bar_offset_x_1, bar_offset_y_1), fill="#77dd77")

    # Left Circle
    draw.ellipse(
        (bar_offset_x - circle_size // 2, bar_offset_y, bar_offset_x + circle_size // 2, bar_offset_y_1), fill="#77dd77")                    

    # Right Circle
    draw.ellipse(
        (bar_offset_x_1 - circle_size // 2, bar_offset_y, bar_offset_x_1 + circle_size // 2, bar_offset_y_1), fill="#77dd77"
    )

    #final_exp 

    text_size = draw.textsize(f"/ {int(200*((1/2)*lvl))} XP", font=mid_font)

    offset_x = 1270 - text_size[0]
    offset_y = bar_offset_y - text_size[1] - 10

    draw.text((offset_x, offset_y), f"/ {int(200*((1/2)*lvl))} XP", font=mid_font, fill="#ffffff")

    #exp
    text_size = draw.textsize(f"{xp}", font=mid_font)
    offset_x -= text_size[0] + 8
    draw.text((offset_x, offset_y), f"{xp}", font=mid_font, fill="#fff")


    # Blitting Name
    #text_size = draw.textsize(ctx.author.name, font=big_font)

    #offset_x = bar_offset_x
    #offset_y = bar_offset_y - text_size[1] - 5
    #draw.text((offset_x , offset_y -240 ), ctx.author.name, font=big_font, fill="#fff")

    # Discriminator
    #offset_x += text_size[0] + 5
    #offset_y += 15

    #draw.text((offset_x , offset_y -240 ), f"#{ctx.author.discriminator}", font=medium_font, fill="#77dd77")

    buffer = BytesIO()
    background.save(buffer, 'png')
#    background.show()
    buffer.seek(0)
    file=discord.File(buffer, filename='latte-level.png')
    
    return file
