import svgwrite




class Plotter():

    def __init__(self):
        self.x = 600
        self.y = 600




    def draw(dataset):
        pass

class DataSet():
    def __init__(self, title, data_list,
                 unit_x, unit_y, interval_x, interval_y):
        """Dataset for drawing"""
        self.title = title
        self.data_list = data_list
        self.unit_x = unit_x
        self.unit_y = unit_y
        self.interval_x = interval_x
        self.interval_y = interval_y
