from abc import ABC, abstractmethod
from ..algorithms.base import Algorithm

class BaseProcesser(ABC):
    """Represents the base class that is responsible of comparing
    detection techniques based on their type.

    Attributes:
        None
    """
    @abstractmethod
    def __call__(self, *args: list, window_size=None, alpha=None, verbose=0) -> None:
        """Runs the comparison of a set of detection techniques.

        This methods executes the necessary action in order to evaluate the
        relative performances of each of the detection techniques.

        Args:
            args (`list` of Algorithm): the detection techiques to be
                compared.
            window_size (`int`): the number of seconds before a time window
                ends.
            alpha (`float`): the value of alpha to be used to compute the
                correcting function.
            verbose (`int`): the level of verbosity. 0 displays nothing,
                1 displays the performances at each step and 2 or higher
                shows the actual comparison made.
        Returns:
            None
        """
        pass

    def report_results(self, algos: list, common_title='Common errors'):
        """Prints out the final results of the comparison.

        This method prints out the final results of the comparison
        of the different techniques.

        Args:
            algos (`list` of Algorithm): the algorithms to be compared.
                the first element represent the actual data.
            common_title (`str`): the header used for printing the results.
        """
        
        print('\n\n[+] Final Error Reporting [+]')
        print('=============================')
        print()
        print(common_title)
        print(''.join(['-' * len(common_title)]))
        for algo in algos:
            algo.reportprint(self.max_name_length)
        print()

    def get_longest_name_length(self, *args) -> int:
        """Sets the length to be used for the techniques' name for printing.

        Given a set of algorithm, this method finds the one with the longest
        name and sets a class variable to it.

        Args:
            *args (`tuple`): the list of detection techniques

        Returns:
            int: the length of the longest name plus 5
        """
        self.max_name_length = max(map(lambda a: len(a.name), args)) + 5
        return self.max_name_length
