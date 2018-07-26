"""High level wrapper for accessing gpu information"""
from py3nvml.py3nvml import *
import sys

class NvidiaGPU():
    """Accesses nvidia information through nvidia-smi"""

    def __init__(self):
        """Init monitoring"""
        self.mintemp = sys.maxsize
        self.maxtemp = sys.maxsize * -1
        self.minclock = sys.maxsize
        self.maxclock = sys.maxsize * -1
        self.minfan = sys.maxsize
        self.maxfan = sys.maxsize * -1
        self.powerMax = sys.maxsize * -1
        self.powerMin = sys.maxsize
        self.gpuUtilMin = sys.maxsize
        self.gpuUtilMax = sys.maxsize * -1
        self.memoryUtilMax = sys.maxsize * -1
        self.memoryUtilMin = sys.maxsize
        self.memoryClockMax = sys.maxsize * -1
        self.memoryClockMin = sys.maxsize
        self.minMemUtil = sys.maxsize
        self.maxMemUtil = sys.maxsize * -1
        nvmlInit()
        self.handle = nvmlDeviceGetHandleByIndex(0)
    def getGpuTemp(self):
        try:
            temp_value = int(str(nvmlDeviceGetTemperature(self.handle,
                                                      NVML_TEMPERATURE_GPU)))
        except NVMLError as e:
            print("Cant get temp:" + e)
            return -273
        self.maxtemp = max(self.maxtemp, temp_value)
        self.mintemp = min(self.mintemp, temp_value)
        return temp_value

    def getGpuClock(self):
        """Get current GPU clock speed in MHZ"""
        try:
            gpuclock = int(str(nvmlDeviceGetClockInfo(self.handle, 1)))
        except NVMLError as e:
            print("Can't get clock:" + e)
            return -1
        self.maxclock = max(self.maxclock, gpuclock)
        self.minclock = min(self.minclock, gpuclock)
        return gpuclock

    def getGpuMemoryClock(self):
        """Get current GPU clock speed in Mhz"""
        memoryclock =int(str(nvmlDeviceGetClockInfo(self.handle, 2)))
        self.memoryClockMax = max(self.memoryClockMax, memoryclock)
        self.memoryClockMin = min(self.memoryClockMin, memoryclock)
        return memoryclock

    def getGpuFanSpeed(self):
        """Get current speed of the fan"""
        gpufan = 0
        gpufan = int(str(nvmlDeviceGetFanSpeed(self.handle)))
        self.maxfan = max(self.maxfan, gpufan)
        self.minfan = min(self.minfan, gpufan)
        return gpufan

    def getGpuPowerUsage(self):
        """Get current power usage in Watts"""
        gpuPower = int(str(nvmlDeviceGetPowerUsage(self.handle)))
        gpuPower = int(round(gpuPower / 1000))
        self.powerMax = max(self.powerMax, gpuPower)
        self.powerMin = min(self.powerMin, gpuPower)
        return gpuPower

    def getGpuUtilization(self):
        """Get utilization percentage"""
        gpuUtil = str(nvmlDeviceGetUtilizationRates(self.handle))
        gpuUtil = gpuUtil.split(",")[0]
        gpuUtil = gpuUtil.replace("c_nvmlUtilization_t(gpu: ", "")
        gpuUtil = gpuUtil.replace(" %", "")
        gpuUtil = int(gpuUtil)
        self.gpuUtilMax = max(self.gpuUtilMax, gpuUtil)
        self.gpuUtilMin = min(self.gpuUtilMin, gpuUtil)
        return gpuUtil

    def getMemoryUtilization(self):
        """Get utilization percentage"""
        memUtil = str(nvmlDeviceGetUtilizationRates(self.handle))
        memUtil = memUtil.split(",")[1].split(": ")[1].split(" ")[0]
        memUtil = int(memUtil)
        self.memoryUtilMax = max(self.memoryUtilMax, memUtil)
        self.memoryUtilMin = min(self.memoryUtilMin, memUtil)
        return memUtil

    def getDeviceName(self):
        """Get nvidia product name"""
        name = str(nvmlDeviceGetName(self.handle))
        return name

    def getDriverVersion(self):
        version = str(nvmlSystemGetDriverVersion())
        return version


if __name__ == '__main__':
    gpu = NvidiaGPU()
    print(gpu.getGpuTemp())
    print(gpu.getGpuClock())
    print(gpu.getGpuMemoryClock())
    print(gpu.getGpuUtilization())
    print(gpu.getMemoryUtilization())
    print(gpu.getDeviceName())
