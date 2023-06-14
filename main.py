from PIL import Image
import numpy as np
import random

GENERATIONS_NUM = 100
POPULATION = 30
WIDTH = 30
HEIGHT = 30

# 画像の読み込み
img_in = Image.open("./Images/twitter.jpg")
img_in = img_in.resize((WIDTH, HEIGHT))

# 出力画像の作成
img_out = Image.new("RGB", (WIDTH, HEIGHT))

# 親世代配列
parent_list = [[] for _ in range(POPULATION)]

# 子世代配列
child_list  = [[] for _ in range(POPULATION)]

# スコア配列
scores = []

# ランダムなドットを生成する関数
def createRandomDots():
    for i in range(POPULATION):
        for h in range(HEIGHT):
            for w in range(WIDTH):
                r = random.randrange(256)
                g = random.randrange(256)
                b = random.randrange(256)
                
                parent_list[i].append([r, g, b])

# スコアを計算する関数
def calcScore():
    global scores, parent_list
    scores = []
    for i in range(POPULATION):
        score = 0
        for h in range(HEIGHT):
            for w in range(WIDTH):
                r, g, b = parent_list[i][h * WIDTH + w]
                r_in, g_in, b_in = img_in.getpixel((w, h))[0], img_in.getpixel((w, h))[1], img_in.getpixel((w, h))[2]
                
                score += (r - r_in) * (r - r_in) + (g - g_in) * (g - g_in) + (b - b_in) * (b - b_in)
        scores.append(score)  
    
    # スコアが低い順(目的画像に近い順)に並べ替え
    parent_list = [i for _, i in sorted(zip(scores, parent_list))]
    scores = sorted(scores)
        
# 次の世代を作成する関数
def createNextGeneration():
    # グローバル変数
    global parent_list, child_list
    
    # 子世代配列を初期化する
    child_list = [[] for _ in range(POPULATION)]
    
    # 生成
    for i in range(POPULATION):
        for h in range(HEIGHT):
            for w in range(WIDTH):
                # 親の選択
                parents = selectParent()
                # 交叉
                r, g, b = parent_list[parents[random.randrange(2)]][h * WIDTH + w]
                # 突然変異 (0.5%)
                if random.randrange(200) == 0:
                    r = random.randrange(256)
                    g = random.randrange(256)
                    b = random.randrange(256)
                
                # 生成されたものを追加する
                child_list[i].append([r, g, b])
        
    # 世代交代
    parent_list = child_list.copy()

# 親個体を2つ選択する関数
def selectParent():
    # (個体数 - 順位)/ 1～個体数の和 で確率を決定
    total = POPULATION * (POPULATION + 1) / 2
    probabilities = [(POPULATION - i) / total for i in range(0, POPULATION)]
    
    # 確率に従って異なる親を2つ選択
    num1, num2 = np.random.choice(POPULATION, size = 2, replace = False, p = probabilities)
    return num1, num2
    
# リストから画像を作成する関数      
def makeImage(dots_list):
    for h in range(HEIGHT):
        for w in range(WIDTH):
            r, g, b = dots_list[h * WIDTH + w]
            img_out.putpixel((w, h), (r, g, b))
           
           
# -------生成処理------- #
    
# 最初の世代を生成                
createRandomDots()

for i in range(GENERATIONS_NUM):    
    calcScore()
    print(i + 1, "世代")
    if (i + 1) % 100 == 0:
        print(scores[0])
        makeImage(parent_list[0])
        img_out.save('./Images/result' + str(i + 1) + '.png')
    createNextGeneration()

# makeImage(parent_list[0])
# img_out.save("result.png")