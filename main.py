from PySide2 import QtWidgets, QtCore, QtGui
from nvidiagpu import NvidiaGPU
import sys


class GpuMonitor(QtWidgets.QWidget):
    """Coolshiit"""

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.top_level_layout = QtWidgets.QVBoxLayout()
        self.layout = QtWidgets.QGridLayout()
        self.name_label = QtWidgets.QLabel("Name")
        self.name_label.setAlignment(QtCore.Qt.AlignTop)
        self.name_label.setStyleSheet("QLabel {color: green}")
        self.driverVersion_label = QtWidgets.QLabel("version")
        self.driverVersion_label.setAlignment(QtCore.Qt.AlignTop)

        # Header row
        self.layout.addWidget(QtWidgets.QLabel("Name"), 0, 0)
        self.layout.addWidget(QtWidgets.QLabel("Current"), 0, 1)
        self.layout.addWidget(QtWidgets.QLabel("Min"), 0, 2)
        self.layout.addWidget(QtWidgets.QLabel("Max"), 0, 3)
        self.layout.addWidget(QtWidgets.QLabel("Unit"), 0, 4)
        # Temperature
        self.layout.addWidget(QtWidgets.QLabel("GPU temprerature: "), 1, 0)
        self.temp_current = QtWidgets.QLabel("0")
        self.temp_min = QtWidgets.QLabel("0")
        self.temp_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.temp_current, 1, 1)
        self.layout.addWidget(self.temp_min, 1, 2)
        self.layout.addWidget(self.temp_max, 1, 3)
        self.layout.addWidget(QtWidgets.QLabel("C"), 1, 4)
        # Fan
        self.fan_name = QtWidgets.QLabel("Fan Speed: ")
        self.layout.addWidget(self.fan_name, 2, 0)
        self.fan_current = QtWidgets.QLabel("0")
        self.fan_min = QtWidgets.QLabel("0")
        self.fan_max = QtWidgets.QLabel("0")
        self.fan_unit = QtWidgets.QLabel("%")
        self.layout.addWidget(self.fan_current, 2, 1)
        self.layout.addWidget(self.fan_min, 2, 2)
        self.layout.addWidget(self.fan_max, 2, 3)
        self.layout.addWidget(QtWidgets.QLabel("%"), 2, 4)
        # Clock
        self.layout.addWidget(QtWidgets.QLabel("GPU Clock: "), 3, 0)
        self.gpu_clock_current = QtWidgets.QLabel("0")
        self.gpu_clock_min = QtWidgets.QLabel("0")
        self.gpu_clock_max = QtWidgets.QLabel("0")
        self.gpu_clock_unit = QtWidgets.QLabel("MHz")
        self.layout.addWidget(self.gpu_clock_current, 3, 1)
        self.layout.addWidget(self.gpu_clock_min, 3, 2)
        self.layout.addWidget(self.gpu_clock_max, 3, 3)
        self.layout.addWidget(QtWidgets.QLabel("MHz"), 3, 4)
        # Utilization
        self.layout.addWidget(QtWidgets.QLabel("GPU Util: "), 4, 0)
        self.gpu_util_current = QtWidgets.QLabel("0")
        self.gpu_util_min = QtWidgets.QLabel("0")
        self.gpu_util_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.gpu_util_current, 4, 1)
        self.layout.addWidget(self.gpu_util_min, 4, 2)
        self.layout.addWidget(self.gpu_util_max, 4, 3)
        self.layout.addWidget(QtWidgets.QLabel("%"), 4, 4)
        # Power
        self.layout.addWidget(QtWidgets.QLabel("GPU Power: "), 5, 0)
        self.gpu_power_current = QtWidgets.QLabel("0")
        self.gpu_power_min = QtWidgets.QLabel("0")
        self.gpu_power_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.gpu_power_current, 5, 1)
        self.layout.addWidget(self.gpu_power_min, 5, 2)
        self.layout.addWidget(self.gpu_power_max, 5, 3)
        self.layout.addWidget(QtWidgets.QLabel("W"), 5, 4)
        #Memory clock
        self.layout.addWidget(QtWidgets.QLabel("Memory Clock: "), 6, 0)
        self.memory_clock_current = QtWidgets.QLabel("Memoryboiis")
        self.memory_clock_min = QtWidgets.QLabel("0")
        self.memory_clock_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.memory_clock_current, 6, 1)
        self.layout.addWidget(self.memory_clock_min, 6, 2)
        self.layout.addWidget(self.memory_clock_max, 6, 3)
        self.layout.addWidget(QtWidgets.QLabel("MHz"), 6, 4)
        #Memory util"GPU Memory Utilization: " + str
        self.layout.addWidget(QtWidgets.QLabel("Memory Util: "), 7, 0)
        self.memory_util_current = QtWidgets.QLabel("0")
        self.memory_util_min = QtWidgets.QLabel("0")
        self.memory_util_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.memory_util_current, 7, 1)
        self.layout.addWidget(self.memory_util_min, 7, 2)
        self.layout.addWidget(self.memory_util_max, 7, 3)
        self.layout.addWidget(QtWidgets.QLabel("%"), 7, 4)
        # Build layout
        self.top_level_layout.addWidget(self.name_label, 0, 0)
        self.top_level_layout.addWidget(self.driverVersion_label, 0, 0)
        self.top_level_layout.addLayout(self.layout, 0)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.top_level_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.top_level_layout)
        self.setMinimumWidth(200)
        self.gpu = NvidiaGPU()


    def show_values(self):
        self.name_label.setText(self.gpu.getDeviceName())
        self.driverVersion_label.setText("Driver version: "
                                         + self.gpu.getDriverVersion())
        # Temp
        self.temp_current.setText(str(self.gpu.getGpuTemp()))
        self.temp_min.setText(str(self.gpu.mintemp))
        self.temp_max.setText(str(self.gpu.maxtemp))
        # Fan
        fan_value = str(self.gpu.getGpuFanSpeed())
        self.fan_current.setText(fan_value)
        self.fan_min.setText(str(self.gpu.minfan))
        self.fan_max.setText(str(self.gpu.maxfan))
        # GPUClock
        self.gpu_clock_current.setText(str(self.gpu.getGpuClock()))
        self.gpu_clock_min.setText(str(self.gpu.minclock))
        self.gpu_clock_max.setText(str(self.gpu.maxclock))
        # Power
        power_value = str(self.gpu.getGpuPowerUsage())
        self.gpu_power_current.setText(power_value)
        self.gpu_power_min.setText(str(self.gpu.powerMin))
        self.gpu_power_max.setText(str(self.gpu.powerMax))
        # Memory clock
        memory_clock = str(self.gpu.getGpuMemoryClock())
        self.memory_clock_current.setText(memory_clock)
        self.memory_clock_min.setText(str(self.gpu.memoryClockMin))
        self.memory_clock_max.setText(str(self.gpu.memoryClockMax))
        # Gpu Util
        gpu_util = str(self.gpu.getGpuUtilization())
        self.gpu_util_current.setText(gpu_util)
        self.gpu_util_min.setText(str(self.gpu.gpuUtilMin))
        self.gpu_util_max.setText(str(self.gpu.gpuUtilMax))
        # Memory util
        memory_util = str(self.gpu.getMemoryUtilization())
        self.memory_util_current.setText(memory_util)
        self.memory_util_min.setText(str(self.gpu.memoryUtilMin))
        self.memory_util_max.setText(str(self.gpu.memoryUtilMax))
        app.processEvents()




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Cute n' VideoCards")

    widget = GpuMonitor()
    widget.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(widget.show_values)
    timer.setInterval(500)
    timer.start()
    sys.exit(app.exec_())
