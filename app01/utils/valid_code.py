import random
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def get_valid_value(request):
    def get_randon_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))     #随机生成三元色，最大值255

    image = Image.new("RGB", (280, 40), get_randon_color())     #RGB是颜色对照表
    draw = ImageDraw.Draw(image)    #给image对象写入文字
    font = ImageFont.truetype("app01/static/font/kumo.ttf", size=35)     #配置字体
    keep_valid_codes = ""
    for i in range(5):
        random_num = str(random.randint(0, 9))      #配置大写小写和数字
        random_lower_alf = chr(random.randint(97, 122))
        random_upper_alf = chr(random.randint(65, 90))
        random_char = random.choice([random_num, random_lower_alf, random_upper_alf])[0]   #返回值为一个列表
        print(random_char, "===")
        draw.text((20 + i * 50, 0), random_char, fill=get_randon_color(), font=font)        #设置xy间距及颜色
        keep_valid_codes += random_char     #拼接

    # 加噪点
    width = 380
    height = 40
    for i in range(140):
        draw.point((random.randint(0,width),random.randint(0,height)),fill=get_randon_color())
    # for i in range(10):
    #     x1=random.randint(0,width)
    #     x2=random.randint(0,width)
    #     y1=random.randint(0,height)
    #     y2=random.randint(0,height)
    #     draw.line((x1,y1,x2,y2),fill=get_randon_color())
    for i in range(100):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=get_randon_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=get_randon_color())

    f = BytesIO()   #数据读写不一定是文件，也可以在内存中读写。验证码没必要保留
    image.save(f, "png")
    data = f.getvalue()
    print("valid_codes:", keep_valid_codes)
    request.session["keep_valid_codes"] = keep_valid_codes  #由于有多个人登录，所以将数据放到session中
    '''
       1  生成随机字符串  1231asd123
       2  set_cookie("sessionid","1231asd123")
       3  django-session
          session_key    session_data
          "1231asd123"   {"keep_valid_codes":"123ab"}
          "3451dfsfd3"   {"keep_valid_codes":"456ab"}
    '''
    return data