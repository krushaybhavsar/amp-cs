import matplotlib.pyplot as plt
import time

class TimingProfiler:
    def __init__(self, algorithms, inputs, trials):
        self.__algorithms = algorithms
        self.__inputs=inputs
        self.__trials=trials
        self.__results=[]

    @property
    def results(self):
      return self.__results

    def single_experiment(self, algorithm):
        totalTime = 0
        data =[]
        for n in self.__inputs:
            for trial in range(self.__trials):
                start = time.perf_counter()
                algorithm(n)
                stop = time.perf_counter()
                elapsedTime = stop-start
                totalTime += elapsedTime
            data.append(totalTime/self.__trials*1000)
        return data

    def run_experiments(self):
        for algorithm in self.__algorithms:
            result={
                "name": algorithm.__name__,
                "data": self.single_experiment(algorithm)
            }
            self.__results.append(result)

    def graph(self, title="", scale="linear"):
        plt.xscale(scale)
        plt.xlabel('n')
        plt.ylabel(f'Time in ms')
        plt.title(title)
        for result in self.__results:
            plt.plot(self.__inputs, result["data"], label = result['name'])
        plt.legend()
        plt.show()
