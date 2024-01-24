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

函数注册时，先创建相应的经验池，然后保存端口的小型经验缓冲区和WITTLE矩阵地址，这里的append即使用上述的浅拷贝方式。

```python
   def registration(self,sim_queue:queue_simulation):
        self.Experience_create(sim_queue.port_index)
        if sim_queue.port_index not in self.registration_port:
            self.registration_port.append(sim_queue.port_index)
            self.port_wittle.append(sim_queue.WITTLE)
            self.port_exp.append(sim_queue.EXP_POOL)
        else:
            index = self.registration_port.index(sim_queue.port_index)
            self.port_wittle[index] = sim_queue.WITTLE
            self.port_exp[index]=sim_queue.EXP_POOL
```

或者使用PYTHON指针操作：https://www.zhihu.com/question/584809823