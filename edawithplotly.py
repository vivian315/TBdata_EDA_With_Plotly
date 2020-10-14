import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import numpy as np

def dataextract(src_file, tg_file, section=50, section_len=10):
    """根据原始数据(src_file)中的price字段，新增两列，一列存储价格区间（price_section）的字符串表示，
        一个字段表示价格区间的排序方法(ps_sort)
    :param section: 价格区间宽度
    :param section_len:价格区间长度，即分成多少段
    :return: 完成后写入新的csv文件(tg_file)
    """
    try:
        tbdata = pd.read_csv(src_file)
        # ps_sort, 价格区间索引
        tbdata.insert(4,"ps_sort",0)
        # price_section, 价格区间 (0,50] 表示 大于0元，小于等于50.00元
        tbdata.insert(5,"price_section","(0,50]")

        i = 1
        while i < section_len:
            if i == section_len-1:
                str_ps = "(%d,~)" % (i * section)
            else:
                str_ps = "(%d,%d]" % (i*section,(i+1)*section)
            tbdata.loc[tbdata.price > i*section, ("ps_sort", "price_section")] = [i, str_ps]
            i += 1
        tbdata.to_csv(tg_file)
    except Exception as e:
        print(e)

def showoverall1():
    """整体数据统计，包括所含商品数、店铺数、价格范围和销量范围"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")
    goods = tbdata["title"].unique()
    stores = tbdata["storeName"].unique()
    pricemax = tbdata["price"].max()
    pricemin = tbdata["price"].min()
    salesmax = tbdata["sales"].max()
    salemin = tbdata["sales"].min()

    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number",
        value=len(goods),
        title={'text': "商品数", "font": {"color": "gold", "size": 20}},
        number={"font": {"color": "gold", "size": 50}},
        domain={"row": 0, "column": 0}
    ))
    fig.add_trace(go.Indicator(
        mode="number",
        value=len(stores),
        title={'text': "店铺数", "font": {"color": "green", "size": 20}},
        number={"font": {"color": "green", "size": 50}},
        domain={"row": 0, "column": 1}
    ))
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=pricemax,
        title={'text': "价格区间", "font": {"color": "blue", "size": 20}},
        number={'prefix': "¥", "font": {"color": "blue", "size": 40}},
        delta={'position': "bottom", 'reference': pricemax - pricemin},
        domain={"row": 0, "column": 2}
    ))
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=salesmax,
        title={'text': "销量区间", "font": {"color": "red", "size": 20}},
        number={"font": {"color": "red", "size": 40}},
        delta={'position': "bottom", 'reference': salesmax - salemin},
        domain={"row": 0, "column": 3}
    ))
    fig.update_layout(
        grid={'rows': 1, 'columns': 4, 'pattern': "independent"})
    fig.show()

def showoverall2():
    """整体数据统计，包括所含商品数、店铺数、价格范围和销量范围"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")

    goods = tbdata["title"].unique()
    stores = tbdata["storeName"].unique()
    pricemax = tbdata["price"].max()
    pricemin = tbdata["price"].min()
    p_median = np.median(tbdata["price"])   #中位数
    p_mean = np.mean(tbdata["price"])       #均值
    p = np.bincount(tbdata["price"])
    p_argmax = np.argmax(p)                   #众数
    price_title = "<span style='color:green'>价格区间 ¥%.2f-¥%.2f</span> <br>" \
                  "<span style='font-size:0.8em;color:red'> 价格中位数：¥%.2f </span><br> " \
                  "<span style='font-size:0.8em;color:teal'>价格众数：¥%.2f <br> 价格均值：¥%.2f</span>" \
                  % (pricemin,pricemax,p_median,p_argmax,p_mean)
    salesmax = tbdata["sales"].max()
    salemin = tbdata["sales"].min()


    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode="number",
        value=len(goods),
        title={"text": "商品数","font": {"color": "gold","size":20}},
        number={"font": {"color": "gold", "size": 50}},
        domain={"row": 0, "column": 0}
    ))
    fig.add_trace(go.Indicator(
        mode="number",
        value=len(stores),
        title={"text": "店铺数", "font": {"color": "green", "size": 20}},
        number={"font": {"color": "green", "size": 50}},
        domain={"row": 1, "column": 0}
    ))
    fig.add_trace(go.Indicator(
        mode="number+delta",
        value=salesmax,
        title={"text": "销量区间", "font": {"color": "red", "size": 20}},
        number={"font": {"color": "red", "size": 40}},
        delta={"position": "bottom", "reference": salesmax - salemin},
        domain={"row": 2, "column": 0}
    ))
    fig.add_trace(go.Indicator(
        mode="gauge",
        title={"text": price_title, "font": {"color": "blue", "size": 20}},
        delta={"position": "bottom", "reference": pricemax - pricemin},
        gauge={"axis":{"range":[0,800]},
               "steps":[{"range": [pricemin, pricemax], "color": "green","thickness":0.65},
                        {"range":[p_argmax, p_mean], "color":"teal"}],
               "threshold":{"line":{"color":"red","width":4},"thickness":1,"value":p_median}
        },
        domain={"row": 1, "column": 1}
    ))
    fig.update_layout(height=500,width=800,
        grid={"rows": 3, "columns": 2, "pattern": "independent"})
    fig.show()

def showbypricesection():
    """价格区间所含商品数，了解维生素的定价"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")
    pricewise = tbdata.groupby(["ps_sort", "price_section"])["title"].count().reset_index()
    fig = go.Figure(go.Bar(x=pricewise["price_section"], y=pricewise["title"],
                           marker={"color": pricewise["title"], "colorscale": "Viridis"}))
    fig.update_layout(title_text="价格区间商品数", xaxis_title="价格区间", yaxis_title="所含商品数")
    fig.show()

def showbypricesection2():
    """价格区间所含商品数（饼图），了解维生素的定价"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")
    pricewise = tbdata.groupby(["price_section"])["title"].count().reset_index()
    fig = go.Figure(go.Pie(labels=pricewise["price_section"], values=pricewise["title"], hole=0.7, rotation=30,
                           hoverinfo="label+percent", textinfo="label+value+percent"))
    fig.update_layout(title_text="价格区间商品占比", xaxis_title="价格区间", yaxis_title="所含商品数")
    fig.show()

def showbypsandsales():
    """各价格区间的销量，了解定价与销量的关系"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")
    pricewise = tbdata.groupby(["ps_sort", "price_section"])["sales"].sum().reset_index()
    fig = go.Figure(go.Bar(x=pricewise["price_section"], y=pricewise["sales"],
                           marker={"color": pricewise["sales"], "colorscale": "Viridis"}))
    fig.update_layout(title_text="价格区间销量", xaxis_title="价格区间", yaxis_title="销量")
    fig.show()

def showbystore():
    """店铺商品数，了解Top N 的展现方法"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")
    storewise = tbdata.groupby("storeName")["title"].count().reset_index()
    storewise = storewise.sort_values("title", ascending=False).reset_index()
    storewise.drop("index", axis=1, inplace=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=storewise["storeName"][:10],
               y=storewise["title"][:10],
               text=storewise["title"][:10],
               name="Top 10",
               marker={"color": storewise["title"][:10], "colorscale": "Earth"}))
    fig.add_trace(
        go.Bar(x=storewise["storeName"][:50],
               y=storewise["title"][:50],
               text=storewise["title"][:50],
               name="Top 50",
               marker={"color": storewise["title"][:50], "colorscale": "Earth"},
               visible=False))

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                active=0,
                x=0.57,
                y=1.2,
                buttons=list([
                    dict(label="Top 10",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Top10 商铺数量店铺"}]),
                    dict(label="Top 30",
                         method="update",
                         args=[{"visible": [False, True]},
                               {"title": "Top30 商铺数量店铺"}]),
                ]),
            )
        ])
    fig.update_traces(textposition="inside")
    fig.update_layout(
        title_text="按店铺商铺数量统计分析",
        xaxis_domain=[0.05, 1.0]
    )
    fig.show()

def showbystoresale():
    """店铺销售量，了解Top N 的展现方法"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")
    storewise = tbdata.groupby("storeName")["sales"].sum().reset_index()
    storewise = storewise.sort_values("sales", ascending=False).reset_index()
    storewise.drop("index", axis=1, inplace=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=storewise["storeName"][:10],
               y=storewise["sales"][:10],
               text=storewise["sales"][:10],
               name="Top 10",
               marker={"color": storewise["sales"][:10], "colorscale": "Earth"}))
    fig.add_trace(
        go.Bar(x=storewise["storeName"][:30],
               y=storewise["sales"][:30],
               text=storewise["sales"][:30],
               name="Top 50",
               marker={"color": storewise["sales"][:30], "colorscale": "Earth"},
               visible=False))

    fig.update_traces(textposition="inside")

    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                active=0,
                x=0.57,
                y=1.2,
                buttons=list([
                    dict(label="Top 10",
                         method="update",
                         args=[{"visible": [True, False]},
                               {"title": "Top10 销量店铺"}]),
                    dict(label="Top 30",
                         method="update",
                         args=[{"visible": [False, True]},
                               {"title": "Top30 销量店铺"}]),
                ]),
            )
        ])
    fig.update_layout(
        title_text="按店铺销售量统计分析",
        xaxis_domain=[0.05, 1.0]
    )
    fig.show()

def showbypriceandstore():
    """销售top7的店铺各价格区间的销量"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")

    top7_stores = ["阿里健康大药房", "康恩贝官方旗舰店", "众久旗舰店", "修正官方旗舰店", "汤臣倍健佰健专卖店官",
                   "希希林保健品专营店", "天猫国际进口超市", "天然博士旗舰店"]
    perc = tbdata.loc[:, ["ps_sort", "price_section", "storeName", "sales"]]
    perc["total_sales"]= perc.groupby([perc.ps_sort, perc.price_section, perc.storeName])["sales"].transform("sum")
    perc.drop("sales", axis=1, inplace=True)
    perc = perc.drop_duplicates()
    perc = perc.sort_values("ps_sort", ascending=True)
    perc = perc.loc[perc["storeName"].isin(top7_stores)]
    perc = perc.sort_values("ps_sort")

    fig = px.bar(perc, x="storeName", y="total_sales",text="total_sales",
                 animation_frame="price_section",animation_group="storeName",
                 hover_name="price_section",
                 range_y=[0, 200000])
    fig.update_traces(textposition="inside")
    fig.update_layout(title_text="Top 7 价格区间销售情况",
                      xaxis_title="店铺名称", yaxis_title="销量")
    fig.show()

def showbypriceandstore2():
    """销售top7的店铺各价格区间的销量，用堆积图展示"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")

    top7_stores = ["阿里健康大药房", "康恩贝官方旗舰店", "众久旗舰店", "修正官方旗舰店", "汤臣倍健佰健专卖店官",
                   "希希林保健品专营店", "天猫国际进口超市", "天然博士旗舰店"]
    perc = tbdata.loc[:, ["ps_sort", "price_section", "storeName", "sales"]]
    perc = perc.groupby([perc.ps_sort, perc.price_section, perc.storeName])["sales"].sum().reset_index()
    perc = perc.loc[perc["storeName"].isin(top7_stores)]
    perc = perc.sort_values("ps_sort")

    fig = go.Figure()
    i=0
    while i<10:
        data = perc[perc.ps_sort == i]
        i += 1
        if len(data)<1:
            continue
        trace_name = data["price_section"].values[0]
        fig.add_trace(go.Bar(x=data["storeName"], y=data["sales"],
                             text=data["sales"], name=trace_name))

    fig.update_traces(textposition="inside")
    fig.update_layout(title_text="Top 7 价格区间销售情况", barmode="relative",
                      xaxis_title="店铺名称", yaxis_title="销量")
    fig.show()

def showwords():
    """商品标题的词云展示，最好用jieba先做分词"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")
    text = list(set(tbdata["title"]))

    wordcloud = WordCloud(font_path="/System/Library/Fonts/PingFang.ttc",
                          max_font_size=50,
                          max_words=50,
                          background_color="white").generate(str(text))

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

def price_sale_comments_scatter():
    """ 用scatter展示统计的价格区间商品数量"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")

    # 一行两列图
    fig = make_subplots(rows=1,cols=2)
    fig.add_trace(go.Scatter(
            y=tbdata["sales"],
            x=tbdata["price"],
            mode="markers",
            name="销量",
            marker=dict(
                color="Teal",
                size=10,showscale=True)),row=1,col=1)
    fig.add_trace(go.Scatter(
            y=tbdata["comments"],
            x=tbdata["price"],
            mode="markers",
            name="评论数",
            marker=dict(
                color="Gold",
                size=10,showscale=True)),row=1,col=2)

    fig.show()

def showprovincegoods():
    """各省商品数量统计"""
    tbdata = pd.read_csv("tb_vitamin_20200925.csv")
    tbdata = tbdata.groupby("province")["title"].count().reset_index()
    tbdata = tbdata.sort_values("title",ascending=True)
    fig = px.bar(tbdata[-20:], y="province", x="title",text="title")

    fig.update_traces(textposition="inside")
    fig.update_layout(title_text="按商铺地域的商品数量统计", barmode="stack",xaxis_title="商品数量", yaxis_title="省市地区")
    fig.show()

if __name__ == "__main__":
    # dataextract("tb_vitamin_01.csv","tb_vitamin_20200925.csv",50,10)
    showoverall2()