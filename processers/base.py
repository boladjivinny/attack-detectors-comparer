from abc import ABC, abstractmethod

class BaseProcesser(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        pass

    def report_results(self, algos):
        for algo in algos:
            print(f'{algo!r}')