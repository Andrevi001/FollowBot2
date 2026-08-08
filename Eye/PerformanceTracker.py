import os
import psutil

class PerformanceTracker():

    class DatiStats():
        def __init__(self, cpuStats: float, ramStats: float):
            self.__cpuStats = cpuStats
            self.__ramStats = ramStats

        def getCpuStats(self) -> float:
            return self.__cpuStats

        def getRamStats(self) -> float:
            return self.__ramStats

    def __init__(self, filePath: str):
        self.__process = psutil.Process()
        self.__process.cpu_percent()
        self.__file = filePath
        self.__CPU_stats = []
        self.__RAM_stats = []
        self.__tot_latencies = []
        self.__inference_latencies = []

    def stats(self) -> DatiStats:
        return self.DatiStats(self.__process.cpu_percent(), self.__process.memory_info().rss / (1024 * 1024))

    def addPerformanceStats(self, tot_latency: float, inference_latency: float) :
        self.__tot_latencies.append(tot_latency)
        self.__inference_latencies.append(inference_latency)
        dati = self.stats()
        self.__CPU_stats.append(dati.getCpuStats())
        self.__RAM_stats.append(dati.getRamStats())


    def writeToFile(self): 
        file_exists = os.path.exists(self.__file)
        with open(self.__file, "a") as file:
            if not file_exists:
                file.write("CPU_Percent,RAM_MB,Total_Latency_ms,Inference_Latency_ms\n")

            for cpu, ram, tot_lat, inf_lat in zip(self.__CPU_stats, self.__RAM_stats, self.__tot_latencies, self.__inference_latencies):
                file.write(f"{cpu},{ram:.2f},{tot_lat:.2f},{inf_lat:.2f}\n")

        self.__CPU_stats.clear()
        self.__RAM_stats.clear()
        self.__tot_latencies.clear()
        self.__inference_latencies.clear()