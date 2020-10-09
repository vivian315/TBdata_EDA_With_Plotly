# TBdata_EDA_With_Plotly

数据为2020年9月25日收集的维生素商品根据销量倒序排列前440条数据

1、数据描述

    nid：商品ID <br>
    title：商品名称及简要宣传性描述 <br>
    price：商品售价 <br>
    sales: 销售量 <br>
    comments：评论数 <br>
    province：店铺所在省 <br>
    city：店铺所在市，直辖市或海外province与city相同 <br>
    storeName：店铺名称 <br>
  
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
