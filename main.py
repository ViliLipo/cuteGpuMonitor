#!/usr/bin/python3
from PySide2 import QtWidgets, QtCore, QtGui
from nvidiagpu import NvidiaGPU, getGpus
import sys


class MainView(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.layout = QtWidgets.QVBoxLayout()
        self.monitors = []
        for gpu in getGpus():
            monitor = GpuMonitor(gpu)
            self.layout.addWidget(monitor)
            self.monitors.append(monitor)
        self.setLayout(self.layout)

    def update(self):
        for monitor in self.monitors:
            monitor.show_values()


class GpuMonitor(QtWidgets.QWidget):
    """Coolshiit"""

    def __init__(self, gpu):
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
        self.layout.addWidget(QtWidgets.QLabel("Avg"), 0, 3)
        self.layout.addWidget(QtWidgets.QLabel("Max"), 0, 4)
        self.layout.addWidget(QtWidgets.QLabel("Unit"), 0, 5)
        # Temperature
        self.layout.addWidget(QtWidgets.QLabel("GPU temprerature: "), 1, 0)
        self.temp_current = QtWidgets.QLabel("0")
        self.temp_min = QtWidgets.QLabel("0")
        self.temp_avg = QtWidgets.QLabel("0")
        self.temp_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.temp_current, 1, 1)
        self.layout.addWidget(self.temp_min, 1, 2)
        self.layout.addWidget(self.temp_avg, 1, 3)
        self.layout.addWidget(self.temp_max, 1, 4)
        self.layout.addWidget(QtWidgets.QLabel("C"), 1, 5)
        # Fan
        self.fan_name = QtWidgets.QLabel("Fan Speed: ")
        self.layout.addWidget(self.fan_name, 2, 0)
        self.fan_current = QtWidgets.QLabel("0")
        self.fan_min = QtWidgets.QLabel("0")
        self.fan_avg = QtWidgets.QLabel("0")
        self.fan_max = QtWidgets.QLabel("0")
        self.fan_unit = QtWidgets.QLabel("%")
        self.layout.addWidget(self.fan_current, 2, 1)
        self.layout.addWidget(self.fan_min, 2, 2)
        self.layout.addWidget(self.fan_avg, 2, 3)
        self.layout.addWidget(self.fan_max, 2, 4)
        self.layout.addWidget(QtWidgets.QLabel("%"), 2, 5)
        # Clock
        self.layout.addWidget(QtWidgets.QLabel("GPU Clock: "), 3, 0)
        self.gpu_clock_current = QtWidgets.QLabel("0")
        self.gpu_clock_min = QtWidgets.QLabel("0")
        self.gpu_clock_avg = QtWidgets.QLabel("0")
        self.gpu_clock_max = QtWidgets.QLabel("0")
        self.gpu_clock_unit = QtWidgets.QLabel("MHz")
        self.layout.addWidget(self.gpu_clock_current, 3, 1)
        self.layout.addWidget(self.gpu_clock_min, 3, 2)
        self.layout.addWidget(self.gpu_clock_avg, 3, 3)
        self.layout.addWidget(self.gpu_clock_max, 3, 4)
        self.layout.addWidget(QtWidgets.QLabel("MHz"), 3, 5)
        # Utilization
        self.layout.addWidget(QtWidgets.QLabel("GPU Util: "), 4, 0)
        self.gpu_util_current = QtWidgets.QLabel("0")
        self.gpu_util_min = QtWidgets.QLabel("0")
        self.gpu_util_avg = QtWidgets.QLabel("0")
        self.gpu_util_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.gpu_util_current, 4, 1)
        self.layout.addWidget(self.gpu_util_min, 4, 2)
        self.layout.addWidget(self.gpu_util_avg, 4, 3)
        self.layout.addWidget(self.gpu_util_max, 4, 4)
        self.layout.addWidget(QtWidgets.QLabel("%"), 4, 5)
        # Power
        self.layout.addWidget(QtWidgets.QLabel("GPU Power: "), 5, 0)
        self.gpu_power_current = QtWidgets.QLabel("0")
        self.gpu_power_min = QtWidgets.QLabel("0")
        self.gpu_power_avg = QtWidgets.QLabel("0")
        self.gpu_power_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.gpu_power_current, 5, 1)
        self.layout.addWidget(self.gpu_power_min, 5, 2)
        self.layout.addWidget(self.gpu_power_avg, 5, 3)
        self.layout.addWidget(self.gpu_power_max, 5, 4)
        self.layout.addWidget(QtWidgets.QLabel("W"), 5, 5)
        # Memory clock
        self.layout.addWidget(QtWidgets.QLabel("Memory Clock: "), 6, 0)
        self.memory_clock_current = QtWidgets.QLabel("Memoryboiis")
        self.memory_clock_min = QtWidgets.QLabel("0")
        self.memory_clock_avg = QtWidgets.QLabel("0")
        self.memory_clock_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.memory_clock_current, 6, 1)
        self.layout.addWidget(self.memory_clock_min, 6, 2)
        self.layout.addWidget(self.memory_clock_avg, 6, 3)
        self.layout.addWidget(self.memory_clock_max, 6, 4)
        self.layout.addWidget(QtWidgets.QLabel("MHz"), 6, 5)
        # Memory util"GPU Memory Utilization: " + str
        self.layout.addWidget(QtWidgets.QLabel("Memory Util: "), 7, 0)
        self.memory_util_current = QtWidgets.QLabel("0")
        self.memory_util_min = QtWidgets.QLabel("0")
        self.memory_util_avg = QtWidgets.QLabel("0")
        self.memory_util_max = QtWidgets.QLabel("0")
        self.layout.addWidget(self.memory_util_current, 7, 1)
        self.layout.addWidget(self.memory_util_min, 7, 2)
        self.layout.addWidget(self.memory_util_avg, 7, 3)
        self.layout.addWidget(self.memory_util_max, 7, 4)
        self.layout.addWidget(QtWidgets.QLabel("%"), 7, 5)
        # Build layout
        self.top_level_layout.addWidget(self.name_label)
        self.top_level_layout.addWidget(self.driverVersion_label)
        self.top_level_layout.addLayout(self.layout)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        self.top_level_layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self.top_level_layout)
        self.setMinimumWidth(200)
        self.gpu = gpu

    def show_values(self):
        self.gpu.update()
        self.name_label.setText(self.gpu.getDeviceName())
        self.driverVersion_label.setText("Driver version: "
                                         + self.gpu.getDriverVersion())
        # Temp
        rec = self.gpu.temp_recorder
        self.temp_current.setText(str(rec.value))
        self.temp_min.setText(str(rec.min))
        self.temp_avg.setText(str(rec.average))
        self.temp_max.setText(str(rec.max))
        # Fan
        rec = self.gpu.fan_recorder
        self.fan_current.setText(str(rec.value))
        self.fan_min.setText(str(rec.min))
        self.fan_avg.setText(str(rec.average))
        self.fan_max.setText(str(rec.max))
        # GPUClock
        rec = self.gpu.gpu_clock_recorder
        self.gpu_clock_current.setText(str(rec.value))
        self.gpu_clock_min.setText(str(rec.min))
        self.gpu_clock_avg.setText(str(rec.average))
        self.gpu_clock_max.setText(str(rec.max))
        # Power
        rec = self.gpu.power_recorder
        self.gpu_power_current.setText(str(rec.value))
        self.gpu_power_min.setText(str(rec.min))
        self.gpu_power_avg.setText(str(rec.average))
        self.gpu_power_max.setText(str(rec.max))
        # Memory clock
        rec = self.gpu.memory_clock_recorder
        self.memory_clock_current.setText(str(rec.value))
        self.memory_clock_min.setText(str(rec.min))
        self.memory_clock_avg.setText(str(rec.average))
        self.memory_clock_max.setText(str(rec.max))
        # Gpu Util
        rec = self.gpu.gpu_util_recorder
        self.gpu_util_current.setText(str(rec.value))
        self.gpu_util_min.setText(str(rec.min))
        self.gpu_util_avg.setText(str(rec.average))
        self.gpu_util_max.setText(str(rec.max))
        # Memory util
        rec = self.gpu.mem_util_recorder
        self.memory_util_current.setText(str(rec.value))
        self.memory_util_min.setText(str(rec.min))
        self.memory_util_avg.setText(str(rec.average))
        self.memory_util_max.setText(str(rec.max))
        app.processEvents()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("Cute GPU Monitor")

    widget = MainView()
    widget.show()
    timer = QtCore.QTimer()
    timer.timeout.connect(widget.update)
    timer.setInterval(500)
    timer.start()
    sys.exit(app.exec_())
