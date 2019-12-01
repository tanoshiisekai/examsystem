from PIL import Image, ImageDraw, ImageFont
import os
import random


def notinposi(posilist, img, tx, ty):
    for i in posilist:
        if abs(i[0] - tx) < img.size[0]//10 and abs(i[1] - ty) < img.size[1]//10:
            return True
    return False


def drawwaterprint(picpath):
    chars = list(
        "ABCDEFGHIJKLMNOPQRSTUVWXYabcdefghijklmnopqrstuvwxyz0123456789")
    cc = 0
    img = Image.open(picpath)
    layer = img.convert("RGBA")
    text_overlay = Image.new("RGBA", layer.size, (255, 255, 255, 0))
    line_overlay = Image.new("RGBA", layer.size, (255, 255, 255, 0))
    posilist = []
    imgsize_x, imgsize_y = img.size
    xcount = imgsize_x // 100
    ycount = imgsize_y // 50
    charcount = xcount * ycount
    while cc < charcount:
        text = random.choice(chars)
        fnt = ImageFont.truetype(
            "C:\Windows\Fonts\simhei.ttf", random.randint(24, 36))
        linerandom = random.random()
        if linerandom > 0.2:
            line_draw = ImageDraw.Draw(line_overlay)
            lxt = random.randint(0, img.size[0])
            lxb = lxt + random.randint(-100, 100)
            lyt = random.randint(0, img.size[1])
            lyb = lyt + random.randint(-100, 100)
            line_draw.line((lxt, lyt) + (lxb, lyb),
                           fill=(random.randint(150, 255), random.randint(150, 200), random.randint(150, 200), 30), width=random.randint(3, 5))
            layer = Image.alpha_composite(layer, line_overlay)
        image_draw = ImageDraw.Draw(text_overlay)
        tsize_x, tsize_y = image_draw.textsize(text, font=fnt)
        tx = random.randint(layer.size[0]//10,
                            int((layer.size[0] - tsize_x) * 0.9))
        ty = random.randint(layer.size[1]//10,
                            int((layer.size[1] - tsize_y) * 0.9))
        while notinposi(posilist, img, tx, ty):
            tx = random.randint(
                layer.size[0]//10,  int((layer.size[0] - tsize_x) * 0.9))
            ty = random.randint(
                layer.size[1]//10, int((layer.size[1] - tsize_y) * 0.9))
        posilist.append((tx, ty))
        image_draw.text((tx, ty), text, font=fnt, fill=(random.randint(
            180, 220), random.randint(180, 220), random.randint(180, 220), 100))
        layer = Image.alpha_composite(layer, text_overlay)
        cc = cc + 1
    layer.save(picpath)

    