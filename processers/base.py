from abc import ABC, abstractmethod

class BaseProcesser(ABC):
    @abstractmethod
    def __call__(self, reference, *args, window_size=None, alpha=None, verbose=0):
        pass

    def report_results(self, algos, common_title='Common errors'):
        
        print('\n\n[+] Final Error Reporting [+]')
        print('=============================')
        print()
        print(common_title)
        print(''.join(['-' * len(common_title)]))
        for algo in algos:
            algo.reportprint(self.max_name_length)
        print()

    def get_longest_name_length(self, *args):
        self.max_name_length = max(map(lambda a: len(a.name), args)) + 5
