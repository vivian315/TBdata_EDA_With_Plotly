# TBdata_EDA_With_Plotly

数据为2020年9月25日收集的维生素商品根据销量倒序排列前440条数据

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

    3、EDA-Exploratory Data Analysis
    3.1 总体统计
    
<details>
<summary>数据统计代码</summary>

```python
    goods = tbdata["title"].unique()
    stores = tbdata["storeName"].unique()
    pricemax = tbdata["price"].max()
    pricemin = tbdata["price"].min()
    salesmax = tbdata["sales"].max()
    salemin = tbdata["sales"].min()
``` 

</details>
 
<details>
    <summary># plotly图形展示代码 </summary>
    
 ``` python
   # plotly图形展示
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
        value=pricemax,
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
    fig.add_trace(go.Indicator(
        mode="number",
        value=len(stores),
        title={'text': "店铺数","font": {"color": "gray","size":20}},
        number={"font": {"color": "gray", "size": 50}},
        domain={"row": 0, "column": 4}
    ))
    fig.update_layout(
        grid={'rows': 1, 'columns': 5, 'pattern': "independent"})
    fig.show()
```    
</details>
    
    图形展示结果, 其中价格从3元到596元，销售数量从800到100K
    ![Overall](https://github.com/vivian315/TBdata_EDA_With_Plotly/blob/main/screenshots/p5.png?raw=true)
