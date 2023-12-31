from PIL import Image
import numpy as np
import time

WIDTH = 30
HEIGHT = 30
ELITE = 1

# 目的画像の指定
file_name = input("ファイル名を入力\n")

# 世代数を指定
generation_num = int(input("世代数 : "))

# 1世代の個体数を指定
population = int(input("1世代の個体数 : "))

# 画像の読み込み
img_in = Image.open('./Images/' + file_name)
img_in = img_in.resize((WIDTH, HEIGHT))

# 出力画像の作成
img_out = Image.new("RGB", (WIDTH, HEIGHT))

# 親世代配列
parent_list = np.empty((population, HEIGHT, WIDTH, 3), int)

# 子世代配列
child_list = np.empty((population, HEIGHT, WIDTH, 3), int)

# スコア配列
scores = np.empty(population, int)

# ランダムなドットを生成する関数
def createRandomDots():
    global parent_list
    parent_list = np.random.randint(0, 256, (population, HEIGHT, WIDTH, 3))

# スコアを計算する関数
def calcScore():
    # グローバル変数
    global scores, parent_list
    # スコア配列を初期化する
    scores = np.empty(population, int)
    
    # 色差を取得する
    diff = parent_list - np.array(img_in)[np.newaxis, :, :, :3]
    # 各色の差を2乗したものを合計した物をスコアにする
    scores = np.sum(np.square(diff), axis=(1, 2, 3))
    
    # スコアが低い順(目的画像に近い順)に並べ替え
    sorted_index = np.argsort(scores)
    parent_list =  parent_list[sorted_index]
    scores = scores[sorted_index]

# 次の世代を作成する関数
def createNextGeneration():
    # グローバル変数
    global parent_list, child_list
    
    # 子世代配列を初期化する
    child_list = np.empty((population, HEIGHT, WIDTH, 3), int)
    
    # エリート保存戦略(前の世代のスコアが高い個体を再利用)
    for i in range(ELITE):
        child_list[i] = parent_list[i]
    
    # 生成
    for i in range(population - ELITE):
        # 親の選択
        parents = selectParent()
        # 交叉
        cross_mask = np.random.randint(2, size = (HEIGHT, WIDTH))
        child = np.where(cross_mask[:, :, np.newaxis], parent_list[parents[0]], parent_list[parents[1]])
        # 突然変異 (0.5%)
        mutation_mask = np.random.choice([False, True], size = (HEIGHT, WIDTH), p = [0.995, 0.005])
        child = np.where(mutation_mask[:, :, np.newaxis], np.random.randint(256, size = 3), child)
        child_list[i + ELITE] = child
    # 世代交代
    parent_list = child_list

# 親個体を2つ選択する関数
def selectParent():
    # (個体数 - 順位)/ 1～個体数の和 で確率を決定
    total = population * (population + 1) / 2
    probabilities = [(population - i) / total for i in range(0, population)]
    
    # 確率に従って異なる親を2つ選択
    num1, num2 = np.random.choice(population, size = 2, replace = False, p = probabilities)
    return num1, num2
    
# リストから画像を作成する関数      
def makeImage(dots_list):
    for h in range(HEIGHT):
        for w in range(WIDTH):
            r, g, b = dots_list[h, w]
            img_out.putpixel((w, h), (r, g, b))
           
           
# -------生成処理------- #
    
# 最初の世代を生成                
createRandomDots()

time_start = time.perf_counter()
for i in range(generation_num):    
    calcScore()
    print(i + 1, "世代")
    if (i + 1) % 100 == 0:
        print(scores[0])
        makeImage(parent_list[0])
        img_out.save('./Images/result' + str(i + 1) + '.png')
    createNextGeneration()
print("経過時間:" + str(time.perf_counter() - time_start))