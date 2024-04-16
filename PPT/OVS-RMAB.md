# OVS-RMAB

OVS代码编译

```
cd ovs-2.16.0
./boot.sh
./configure --with-dpdk=static CFLAGS="-Ofast -msse4.2 -mpopcnt"
make -j     # 多线程编译
sudo make install
```

Pktgen 和 testpmd 测试

