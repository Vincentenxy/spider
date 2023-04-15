# 多线程&线程池


from concurrent.futures import ThreadPoolExecutor

# 多线程类
class MultiThreads:
    max_workers = 8
    thread_instance = None

    def __init__(self, t_max_worker=8):
        MultiThreads.max_workers = t_max_worker


    # 返回线程池实例
    def get_instance(self):
        if MultiThreads.thread_instance is None:
            MultiThreads.thread_instance = ThreadPoolExecutor(MultiThreads.max_workers)
        return MultiThreads.thread_instance


