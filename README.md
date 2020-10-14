# TBdata_EDA_With_Plotly

    本文为根据2020年9月25日收集的TB维生素商品根据销量倒序排列前440条数据进行的探索性数据分析
    python: 3.7.7
    plotly: 4.11.0
    
    数据文件参照:tb_vitamin_20200925.csv
    代码文件参照：edawithplotly.py

1、数据描述

    nid：商品ID 
    title：商品名称及简要宣传性描述 
    price：商品售价 
    sales: 销售量 
    comments：评论数 
    province：店铺所在省 
    city：店铺所在市，直辖市或海外province与city相同 
    storeName：店铺名称 
  
2、导入数据文件
  ```python
  Import pandas as pd
  tbdata = pd.read_csv("tb_vitamin_20200925.csv")
  ```
  ```python
  # 数据纬度和大小
  print("数据纬度：  ",  tbdata.shape)
  print("数据大小：  ", tbdata.size)
  ```
    数据纬度：   (440, 12) 
    数据大小：   5280

3、数据整理
    为了统计需要，将价格整理成价格区间，新增两列，价格区间索引和价格区间字符串
    
<details>
    <summary> 代码 </summary>
    
``` python
# ps_sort, 价格区间索引
tbdata.insert(3,"ps_sort",0)
# price_section, 价格区间 (0,50] 表示 大于0元，小于等于50.00元
tbdata.insert(4,"price_section","(0,50]")

#根据price的值，填充ps_sort和 price_section列
i = 1
while i < 10:
    if i == 9:
        str_ps = "(%d,~)" % (i * 50)
    else:
        str_ps = "(%d,%d]" % (i*50,(i+1)*50)
    tbdata.loc[tbdata.price > i*50, ("ps_sort", "price_section")] = [i, str_ps]
    i += 1

#将整理好的数据写入新的csv文件
tbdata.to_csv("tb_vitamin_02.csv")    
```
</details>
   
4、EDA-Exploratory Data Analysis <br>
4.1 总体统计
其中,440条数据中商品数430个，店铺178家，价格从3元到596元，销售数量从800到100K

   ![Overall](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p4.png?raw=true)

<details>
    <summary> 点击展开代码 </summary>

``` python
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
    title={'text': "商品数","font": {"color": "gold","size":20}},
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
```    
</details>
其中,价格中位数、众数、均值均低于90元

   ![Overall](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p19.png?raw=true)
   
<details>
    <summary> 点击展开代码 </summary>
    
``` python    
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
```
</details>
4.2 价格区间分析
4.2.1 按价格区间统计商品数量
        图表如下，说明维生素价格主要在200元以下，其中50元以下最多
![按价格区间](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p5.png?raw=true)
    
<details>
<summary>点击展开代码</summary>
    
``` python
    pricewise = tbdata.groupby(['ps_sort', 'price_section'])['title'].count().reset_index()
    fig = go.Figure(go.Bar(x=pricewise['price_section'], y=pricewise['title'],
                           marker={'color': pricewise['title'], 'colorscale': 'Viridis'}))
    fig.update_layout(title_text='价格区间商品数', xaxis_title='价格区间', yaxis_title='所含商品数')
    fig.show()
```
</details>


        或用饼图展示
![按价格区间](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p6.png?raw=true)
   
<details>
<summary>点击展开饼图代码</summary>
    
``` python

pricewise = tbdata.groupby(['price_section'])['title'].count().reset_index()
fig = go.Figure(go.Pie(labels=pricewise['price_section'], values=pricewise['title'], hole=0.7, rotation=30,
                   hoverinfo="label+percent", textinfo="label+value+percent"))
fig.update_layout(title_text='价格区间商品占比')
fig.show()

```
</details>

4.2.2 按价格区间统计维生素的销售量
图表如下，说明维生素销售量与商品数一致，主要集中在价格200元以下的，其中50元以下最多
![按价格区间](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p7.png?raw=true)
    
<details>
    <summary> 点击展开代码 </summary>
    
```python    
    pricewise = tbdata.groupby(['ps_sort', 'price_section'])['sales'].sum().reset_index()
    fig = go.Figure(go.Bar(x=pricewise['price_section'], y=pricewise['sales'],
                           marker={'color': pricewise['sales'], 'colorscale': 'Viridis'}))
    fig.update_layout(title_text='价格区间销量', xaxis_title='价格区间', yaxis_title='销量')
    fig.show()    
```
</details>

4.2.3 销量和评论数与价格关系
图标如下，维生素销售量和评论主要集中在价格200元以下的，销售量集中在20K以下，评论集中在50K以下，价格50元以下销量和评论数都较高
![按价格区间](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p17.png?raw=true)

<details>
    <summary>点击展开代码</summary>
    
```python   
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
```
    
</details>

4.3 按店铺分析

    4.3.1 店铺商品数量统计
    图表如下，除了阿里健康大药房的商品种类达78种，前十店铺中商品集中在7-20中，前30店铺中大多只有2～5中维生素产品
    
<img src="https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p8.png" width="450" alt="按店铺" /> <img src="https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p9.png" width="450" alt="按店铺" />
      
<details>
    <summary> 点击展开代码 </summary>
    
```python
    
    storewise = tbdata.groupby('storeName')['title'].count().reset_index()
    storewise = storewise.sort_values('title', ascending=False).reset_index()
    storewise.drop("index", axis=1, inplace=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=storewise['storeName'][:10],
               y=storewise['title'][:10],
               name='Top 10',
               marker={'color': storewise['title'][:10], 'colorscale': 'Earth'}))
    fig.add_trace(
        go.Bar(x=storewise['storeName'][:30],
               y=storewise['title'][:30],
               name='Top 30',
               marker={'color': storewise['title'][:30], 'colorscale': 'Earth'},
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
    fig.update_layout(
        title_text="按店铺商铺数量统计分析",
        xaxis_domain=[0.05, 1.0]
    )
    fig.show()
    
```
</details>

    4.3.3 店铺商品销量统计
    图表如下，阿里健康大药房商品种类和销量都名列第一，众久旗舰店只有7款产品却贡献126k的销售量，希希林保健品只售2款产品却达到57K销量
    
<img src="https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p10.png" width="450" alt="按店铺" /> <img src="https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p11.png" width="450" alt="按店铺" />
      
<details>
    <summary> 点击展开代码 </summary>
    
```python
    storewise = tbdata.groupby('storeName')['sales'].sum().reset_index()
    storewise = storewise.sort_values('sales', ascending=False).reset_index()
    storewise.drop("index", axis=1, inplace=True)

    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=storewise['storeName'][:10],
               y=storewise['sales'][:10],
               text=storewise['sales'][:10],
               name='Top 10',
               marker={'color': storewise['sales'][:10], 'colorscale': 'Earth'}))
    fig.add_trace(
        go.Bar(x=storewise['storeName'][:30],
               y=storewise['sales'][:30],
               text=storewise['sales'][:30],
               name='Top 30',
               marker={'color': storewise['sales'][:30], 'colorscale': 'Earth'},
               visible=False))

    fig.update_traces(textposition='inside')

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
```

</details>

4.4 价格区间与店铺销量关系

    图表如下，无商品定价于250～300价格段，阿里健康大药房和天猫国际进口超市各价格段商品均有分布，其它店家基本只有1到2个价格段产品
    
<img src="https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p12.png" width="450" /> <img src="https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p13.png" width="450" />
<img src="https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p14.png" width="450"  /> <img src="https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p15.png" width="450" />
      
<details>
    <summary> 点击展开代码 </summary>
    
```python 
top7_stores = ['阿里健康大药房', '康恩贝官方旗舰店', '众久旗舰店', '修正官方旗舰店', '汤臣倍健佰健专卖店官',
           '希希林保健品专营店', '天猫国际进口超市', '天然博士旗舰店']
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
fig.update_traces(textposition='inside')
fig.update_layout(title_text="Top 7 价格区间销售情况",
              xaxis_title='店铺名称', yaxis_title='销量')
fig.show()
```
    
``` python
# 堆积图代码
top7_stores = ['阿里健康大药房', '康恩贝官方旗舰店', '众久旗舰店', '修正官方旗舰店', '汤臣倍健佰健专卖店官',
               '希希林保健品专营店', '天猫国际进口超市', '天然博士旗舰店']
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

fig.update_traces(textposition='inside')
fig.update_layout(title_text="Top 7 价格区间销售情况", barmode="relative",
                  xaxis_title='店铺名称', yaxis_title='销量')
fig.show()  
```
</details>

4.5 分词
    商品名称的词云
    词云显示如下，可见除了常见维生素b6，b2等，在商品名称中多包含容量数，以及买n送n宣传
    ![词云](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p16.png?raw=true)
   
<details>
    <summary> 点击展开代码 </summary>

```python
    text = list(set(tbdata["title"]))
    #注意指定中文词库否则中文不能正确显示
    wordcloud = WordCloud(font_path="/System/Library/Fonts/PingFang.ttc",
                          max_font_size=50,
                          max_words=50,
                          background_color="white").generate(str(text))

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
```  
</details>

4.6 按区域统计

可见商铺大陆主要集中在广东、浙江、上海和江苏，大陆以外主要是澳大利亚香港
![区域](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p18.png?raw=true)
   
<details>
    <summary> 点击展开代码 </summary>

```python
    tbdata = tbdata.groupby("province")["title"].count().reset_index()
    tbdata = tbdata.sort_values("title",ascending=True)
    fig = px.bar(tbdata[-20:], y="province", x="title",text="title")

    fig.update_traces(textposition="inside")
    fig.update_layout(title_text="按商铺地域的商品数量统计", barmode="stack",xaxis_title="商品数量", yaxis_title="省市地区")
    fig.show()
```  
</details>
