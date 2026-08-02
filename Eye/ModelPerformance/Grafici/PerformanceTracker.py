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
        self.__tot_latency = 0.0
        self.__inference_latency = 0.0

    def stats(self) -> DatiStats:
        return self.DatiStats(self.__process.cpu_percent(), self.__process.memory_info().rss / (1024 * 1024))

    def thisLatency(self, latency: float):
        self.__tot_latency = latency

    def thisInferenceLatecy(self, latency: float):
        self.__inference_latency = latency

    def writeToFile(self): 
        dati = self.stats()

        file_exists = os.path.exists(self.__file)
        with open(self.__file, "a") as file:
            if not file_exists:
                file.write("CPU_Percent,RAM_MB,Total_Latency_ms,Inference_Latency_ms\n")
            file.write(f"{dati.getCpuStats()},{dati.getRamStats():.2f},{self.__tot_latency:.2f},{self.__inference_latency:.2f}\n")