from abc import ABC, abstractmethod

class BaseProcesser(ABC):
    @abstractmethod
    def __call__(self, reference, *args, window_size=None, alpha=None, verbose=0):
        pass

    def report_results(self, algos):
        for algo in algos:
            print(f'{algo!r}')