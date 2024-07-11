from matplotlib import pyplot as plt
from os import getcwd
import matplotlib.ticker as ticker




# для работы функции нужны координаты x и y(по-отдельности, иначе придется менять алгоритм построения графика),
# а также значения сторон или другие данные, которые должны быть в окне
# def mkimg(sides = [],x = [],y = [],savedir = ""):
def mkimg(sides, x, y, user_id):
    x= [0,x,sides[2]]
    y=[0,y,0]

#      cab
    extremex = [min(x), max(x)] #крайние значения x
    extremey = [min(y), max(y)]  # крайние значения y
    maxscale = 0
    for i in extremex:
        if abs(i) > maxscale:
            maxscale = abs(i)
    for i in extremey:
        if abs(i) > maxscale:
            maxscale = abs(i)

    fig = plt.figure(figsize=(10,10))
    fig.patch.set_facecolor("#f2f0f1")# цвет заднего фона
    ax = fig.add_subplot()#координатная плоскость
    if extremex[0] >= 0:
        plt.xlim(-maxscale*0.1,maxscale*1.1)
        plt.ylim(-0.1*maxscale,maxscale*1.1)
    else:
        plt.xlim(-maxscale * 1.2, maxscale * 1.1)
        plt.ylim(-0.1 * maxscale, maxscale * 2.2)

    ax.set(facecolor = "#f2f0f1")
    ax.plot(x[0:2], y[0:2], label="AB", color="#FF4500")  # строит отрезки AB,BC,AC по точкам
    ax.plot(x[1:3], y[1:3], label="BC", color="#FF4500")
    ax.plot([x[2], x[0]], [y[2], y[0]], label="AC", color="#FF4500")
    ax.xaxis.set_major_locator(ticker.FixedLocator(x + [0]))  # обозначение координат вершин на осях
    ax.yaxis.set_major_locator(ticker.FixedLocator(y + [0]))


    plt.xticks(fontsize = 14)
    plt.yticks(fontsize = 14)


    apexes = "ABC"
    '''
    for i in range(3):# обозначение вершин треугольника(требует доработки)
        if y[i] == extremey[1]:
            ax.annotate(apexes[i],[x[i], y[i]+(extremey[1] - extremey[0])/100], size = 20)
            continue
        if x[i] == extremex[1]:
            ax.annotate(apexes[i],[x[i]+(extremex[1] - extremex[0])/90, y[i]], size = 20)
            continue
        if x[i] == extremex[0]:
            ax.annotate(apexes[i],[x[i]-(extremex[1] - extremex[0])/5, y[i]], size = 20)
            continue

        if y[i] == extremey[0]:
            ax.annotate(apexes[i],[x[i], y[i]-(extremey[1] - extremey[0])/30], size = 20)
            continue
    '''
    ax.annotate("C", [-0.055*maxscale,0], size = 20)
    ax.annotate("B", [x[1], 1.01*y[1]], size=20)
    ax.annotate("A", [x[2]*1.005, 0], size=20)
    ax.grid()# сетка координат
    ax.legend(["BC = "+str(sides[0]),"AB = "+str(sides[1]),"AC = "+str(sides[2])], fontsize = 14)# табличка со значениями


    savedir = getcwd() + f"/image/image{user_id}.png"
    plt.savefig(savedir, dpi = 150)
    return savedir



mkimg(sides = [34,57.9,24], x = -33.759, y = 4.045 ,user_id="abc")
