# TBdata_EDA_With_Plotly

数据为2020年9月25日收集的维生素商品根据销量倒序排列前440条数据, 数据文件参照tb_vitamin_20200925.csv

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

4.2 按价格区间统计商品数量
    图表如下，说明维生素价格主要在200元以下，其中50元以下最多
    ![Overall](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p5.png?raw=true)
    
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
   ![Overall](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p6.png?raw=true)
   
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

4.3 按价格区间统计维生素的销售量
    图表如下，说明维生素销售量与商品数一致，主要集中在价格200元以下的，其中50元以下最多
    ![Overall](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p7.png?raw=true)
    
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
