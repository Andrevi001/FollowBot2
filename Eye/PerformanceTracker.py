import os
import psutil

class PerformanceTracker():
    """
    Class designed for tracking performance information of a given main loop. 
    
    Metrics collected include: CPU percentage, RAM usage, latency of a cycle and inference latency.
    """

    class StatsData():
        """Internal class designed to store CPU and RAM usage stats"""

        def __init__(self, cpuStats: float, ramStats: float):
            """Class constructor"""

            self.__cpuStats = cpuStats
            self.__ramStats = ramStats

        def getCpuStats(self) -> float:
            """
            Used to obtain CPU usage stats

            Returns:
                float: CPU usage stats
            """
            return self.__cpuStats

        def getRamStats(self) -> float:
            """
            Used to obtain RAM usage stats
            """
            return self.__ramStats

    def __init__(self, filePath: str):
        """
        Class constructor
        
        Args:
            filePath: str, indicates where to save collected data
        """

        self.__process = psutil.Process()
        self.__process.cpu_percent()
        self.__file = filePath
        self.__CPU_stats = []
        self.__RAM_stats = []
        self.__tot_latencies = []
        self.__inference_latencies = []

    def stats(self) -> StatsData:
        """
        Used to obtain current CPU and Ram usage stats.
        
        Returns:
            StatsData: CPU and Ram usage stats
        """

        return self.StatsData(self.__process.cpu_percent(), self.__process.memory_info().rss / (1024 * 1024))

    def addLatencyStats(self, tot_latency: float, inference_latency: float) :
        """
        Appends loop and inference latency measurements alongside CPU/RAM metrics.
        
        Args:
            tot_latency: float, indicates the measured latency of the main execution loop.
            inference_latency: float, indicates the measured inference latency of the model under examination.
        """

        self.__tot_latencies.append(tot_latency)
        self.__inference_latencies.append(inference_latency)
        dati = self.stats()
        self.__CPU_stats.append(dati.getCpuStats())
        self.__RAM_stats.append(dati.getRamStats())


    def writeToFile(self):
        """Appends collected data in the CSV file pointed by self.__file and clears internal buffers"""

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