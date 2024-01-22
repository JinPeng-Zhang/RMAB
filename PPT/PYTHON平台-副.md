PYTHON

list类型append添加函数，[Python 列表 append()函数使用详解-CSDN博客](https://blog.csdn.net/wangyuxiang946/article/details/122142534)

函数实际逻辑为**浅拷贝**，即添加的为对象地址而非内容，当对象内容发生改变时，append主体内容也随之改变

```c
list1 = ['zhangsan']
a = [1,2,3]
list1.append(a)  # 列表list1添加列表a
print(list1)
a.append(4)  # 列表a发生变化
list1.append(a)
print(list1)  # 列表list1也会同步变化

输出：

['zhangsan', [1, 2, 3]]
['zhangsan', [1, 2, 3, 4], [1, 2, 3, 4]]
```

该函数特性，适合用于实现模型"配置API"的注册功能