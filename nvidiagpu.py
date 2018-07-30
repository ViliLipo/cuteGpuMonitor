"""High level wrapper for accessing gpu information"""
from py3nvml.py3nvml import *
import sys
from math import floor


class NvidiaGPU():
    """Accesses nvidia information through nvidia-smi"""

    def __init__(self):
        """Init monitoring"""
        self.recorders = []
        self.temp_recorder = ValueRecorder(self.getGpuTemp)
        self.recorders.append(self.temp_recorder)
        self.gpu_clock_recorder = ValueRecorder(self.getGpuClock)
        self.recorders.append(self.gpu_clock_recorder)
        self.memory_clock_recorder = ValueRecorder(
                self.getGpuMemoryClock)
        self.recorders.append(self.memory_clock_recorder)
        self.fan_recorder = ValueRecorder(self.getGpuFanSpeed)
        self.recorders.append(self.fan_recorder)
        self.power_recorder = ValueRecorder(self.getGpuPowerUsage)
        self.recorders.append(self.power_recorder)
        self.gpu_util_recorder = ValueRecorder(self.getGpuUtilization)
        self.recorders.append(self.gpu_util_recorder)
        self.mem_util_recorder = ValueRecorder(self.getMemoryUtilization)
        self.recorders.append(self.mem_util_recorder)
        nvmlInit()
        self.handle = nvmlDeviceGetHandleByIndex(0)

    def update(self):
        """Updates the values for recorders"""
        for recorder in self.recorders:
            recorder.update()
        self.getPerfCapReason()

    def getGpuTemp(self):
        try:
            temp_value = int(str(nvmlDeviceGetTemperature(self.handle,
                                                      NVML_TEMPERATURE_GPU)))
        except NVMLError as e:
            print("Cant get temp:" + e)
            return -273
        return temp_value

    def getGpuClock(self):
        """Get current GPU clock speed in MHZ"""
        try:
            gpuclock = int(str(nvmlDeviceGetClockInfo(self.handle, 1)))
        except NVMLError as e:
            print("Can't get clock:" + e)
            return -1
        return gpuclock

    def getGpuMemoryClock(self):
        """Get current GPU clock speed in Mhz"""
        memoryclock = int(str(nvmlDeviceGetClockInfo(self.handle, 2)))
        return memoryclock

    def getGpuFanSpeed(self):
        """Get current speed of the fan"""
        gpufan = 0
        gpufan = int(str(nvmlDeviceGetFanSpeed(self.handle)))
        return gpufan

    def getGpuPowerUsage(self):
        """Get current power usage in Watts"""
        gpuPower = int(str(nvmlDeviceGetPowerUsage(self.handle)))
        gpuPower = int(round(gpuPower / 1000))
        return gpuPower

    def getGpuUtilization(self):
        """Get utilization percentage"""
        gpuUtil = str(nvmlDeviceGetUtilizationRates(self.handle))
        gpuUtil = gpuUtil.split(",")[0]
        gpuUtil = gpuUtil.replace("c_nvmlUtilization_t(gpu: ", "")
        gpuUtil = gpuUtil.replace(" %", "")
        gpuUtil = int(gpuUtil)
        return gpuUtil

    def getMemoryUtilization(self):
        """Get utilization percentage"""
        memUtil = str(nvmlDeviceGetUtilizationRates(self.handle))
        memUtil = memUtil.split(",")[1].split(": ")[1].split(" ")[0]
        memUtil = int(memUtil)
        return memUtil

    def getDeviceName(self):
        """Get nvidia product name"""
        name = str(nvmlDeviceGetName(self.handle))
        return name

    def getDriverVersion(self):
        version = str(nvmlSystemGetDriverVersion())
        return version

    def getPerfCapReason(self):
        reasons = {0: "None", 1: "GPU Idle", 2: "Application settings",
                   4: "Software powercap", 8: "Hardware slowdown"
                 }
        print(nvmlDeviceGetCurrentClocksThrottleReasons(self.handle))
        return reasons[nvmlDeviceGetCurrentClocksThrottleReasons(self.handle)]


class ValueRecorder():
    def __init__(self, func):
        self.min = sys.maxsize
        self.max = sys.maxsize * -1
        self.sum = 0
        self.count = 0
        self.function = func
        self.value = 0
        self.average = 0

    def update(self):
        self.value = self.function()
        self.min = min(self.value, self.min)
        self.max = max(self.value, self.max)
        try:
            self.sum = self.sum + self.value
            self.count = self.count + 1
            self.average = int(round(self.sum/self.count, 0))
        except OverflowError:
            self.sum = int(floor(self.sum/1000))
            self.count = int(floor(self.count/1000))







if __name__ == '__main__':
    gpu = NvidiaGPU()
    print(gpu.getGpuTemp())
    print(gpu.getGpuClock())
    print(gpu.getGpuMemoryClock())
    print(gpu.getGpuUtilization())
    print(gpu.getMemoryUtilization())
    print(gpu.getDeviceName())
