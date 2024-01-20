## 最新版本平台路径

https://github.com/JinPeng-Zhang/RMAB/tree/main/RMAB-project/WITTLE%20INDEX

### 仿真平台实现框架参照：“ECN-WI - 副本.pptx”中“更新逻辑“框架图

框架内容：

```json
queue_simulation{
	priority_queue{
		Priority_NUM:8
		QUEUE:LIST[20]
		queue_siez:20
		Congestion_handling:["ECN","AQM","FULL_DROP"]
		Arrival_probability:LIST[8]
		....
	}
	state_Collect:FUCTION()
	Scheduling_algorithm{
        
    }
}


```

```json
configure API{
	Experience_upload:FUCTION()
	WITTLE_UPDATE:FUCTION()
}
```

```json
experience_pool{
	file1,
	file2,
	....
	filen,
	conf_file
}
```

```
WITTLE_INDEX_MODEL{

}
```

| 1/17-1/18                                |
| ---------------------------------------- |
| 1.算法模型设计                           |
| 2.重构仿真代码模块、调度器、队列、比较器 |
| 3.发包收包测试                           |

| 1/19    |
| ------- |
| PPT整理 |



| 1/20-1/21                                                    |
| ------------------------------------------------------------ |
| 1.修改ECN,AQM Congestion_handling函数(离散->连续，此时刻队列数据包->此时刻达到数据包)，修改MDP类（数据处理模块） |
| 2.完成experience_pool文件模块设计、实现状态收集以及经验收集  |
| 3.完成configure API模块设计                                  |
| 4.功能测试                                                   |
| 5.文档                                                       |

| 1-21                           |
| ------------------------------ |
| 1.模块联调测试                 |
| 2.统计初始数据，完成WITTLE计算 |
| 3.设计测试计划                 |

仿真平台搭建过程中没有对变量进行安全检查，潜在一些BUG