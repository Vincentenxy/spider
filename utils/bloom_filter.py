# 布隆过滤器有两种实现
# 1.使用内存
# 2.使用redis
from pybloom_live import ScalableBloomFilter, BloomFilter


# 利用内存实现布隆过滤器
class BloomFilter:

    # 生成一个可变长度的过滤器
    comm_filter = ScalableBloomFilter(initial_capacity=100000, error_rate=0.001)

    # 每个实例可以自定义一个自身的filter
    filters_dic = {}

    def __init__(self, filter_name='', init_capacity=10000, err_rate=0.001):
        if filter_name == '':
            return
        if BloomFilter.filters_dic[filter_name] is None:
            BloomFilter.filters_dic[filter_name] = ScalableBloomFilter(init_capacity, err_rate)
        self.filter = BloomFilter.filters_dic[filter_name]

    # 启动时从数据库中初始化布隆过滤器
    def init_filters(self):
        # TODO 从redis或者mysql中初始化comm_filter和filters_dic
        pass

    def get_filter(self):
        return BloomFilter.comm_filter



# 使用redis实现布隆过滤器
# redis 中需要安装RedisBloom插件
class BloomFilterRedis:

    def __init__(self):
        pass




bloom_filter = BloomFilter()
bloom_filter.get_filter().add('1212')
print('1212' in bloom_filter.get_filter())
print('1213' in bloom_filter.get_filter())
print(bloom_filter.get_filter())