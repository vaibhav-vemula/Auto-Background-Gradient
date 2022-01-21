from PIL import Image,ImageChops,ImageFilter
import os

thickness = 3   # Thickness of shadow
comp = False    # Complement of dominant color(True - Bg is set to dominant color, False - Bg is set to Complement color)

def dominantColor(img):
    
    (width, height) = img.size
    rt, gt, bt = 0,0,0
    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x,y))
            rt += r
            gt += g
            bt += b
            count += 1
    return (int(rt/count), int(gt/count), int(bt/count))


def fff(ffimg, border):
    
    # ffimg.show('bla')
    w = ffimg.size[0]
    h = ffimg.size[1]
    
    q1 = dominantColor(ffimg.crop((0,0,w/2,h/2)))
    q2 = dominantColor(ffimg.crop((w/2,0,w,h/2)))
    q3 = dominantColor(ffimg.crop((0,h/2,w/2,h)))
    q4 = dominantColor(ffimg.crop((w/2,h/2,w,h)))
    
    w = ffimg.size[0] + 2 * border
    h = ffimg.size[1] + 2 * border
    
    img = Image.new('RGB', (w,h))
    for i in range(w):
        for j in range(h):
            img.putpixel((i,j), q1)
    # img.show('img1')

    img2 = Image.new('RGBA', (w,h))
    for i in range(w):
        for j in range(h):
            img2.putpixel((i,j), q2)
    # img2.show('img2')
    
    img3 = Image.new('RGB', (w,h))
    for i in range(w):
        for j in range(h):
            img3.putpixel((i,j), q3)
    # img3.show('img3')
    
    img4 = Image.new('RGB', (w,h))
    for i in range(w):
        for j in range(h):
            img4.putpixel((i,j), q4)
    # img4.show('img4')
    
    mask = Image.new('L', (w, h))
    mask_data = []
    for y in range(h):
        for x in range(w):
            mask_data.append(int(255 * (x / h)))
    mask.putdata(mask_data)

    img.paste(img2, (0, 0), mask)
    img3.paste(img4, (0,0), mask)

    # img.paste(img3,(0,0), mask)
    
    # img = img.crop((0,0,img.size[0],img.size[1]/2))
    # img3 = img3.crop((0,0,img3.size[0],img3.size[1]/2))
    
    mask2 = Image.new('L', (img.width, img.height))
    mask_data2 = []
    for y in range(img.height):
        for x in range(img.width):
            mask_data2.append(int(255 * (y /img.height)))
    mask2.putdata(mask_data2)
    mask2 = mask2.rotate(180)
    # mask2.show()
    
    immm = Image.composite(img, img3, mask2)
    # immm.show()
    
    return immm

def gradient(new_width,new_height, dom_color):
    base = Image.new('RGB', (new_width, new_height), (dom_color[0]+90, dom_color[1]+90, dom_color[2]+90))
    topp = Image.new('RGB', (new_width, new_height),dom_color )
    mask = Image.new('L', (new_width, new_height))
    mask_data = []
    for y in range(new_height):
        for x in range(new_width):
            mask_data.append(int(255 * (y / new_height)))
    mask.putdata(mask_data)
    base.paste(topp, (0, 0), mask)
    return base

def dropShadow(img,dom_color, iterations = 9, border = 90, shadow_colour = 0x333333): 
    shadow = fff(img, border)
    # shadow.show('ffff')
    shadow.paste(shadow_colour, [border-thickness, border-thickness+6, border + img.size[0]+thickness, border + img.size[1]+thickness])
    for _ in range(iterations):
        shadow = shadow.filter(ImageFilter.BLUR)
    shadow.paste(img, (border, border))
    return shadow  

def backgroundPadding(img):
    dom_color = dominantColor(img)
    base = dropShadow(img,dom_color)
    return base

# imgg = Image.open("entre.jpg")
# backgroundPadding(imgg).save("out.jpg")

for root, _, files in os.walk('images',topdown=False):
    for file in files:
        imgg = Image.open(os.path.join(root,file))
        backgroundPadding(imgg).save("output/"+file)