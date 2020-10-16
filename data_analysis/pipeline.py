from data.data import Data
from analysis.analysis import Analysis


class Pipeline:
    def __init__(self):
        self.data: Data or None = None
        self.analysis: Analysis or None = None

    def get_data(self):
        self.data = Data()

    def run_analysis(self):
        self.analysis = Analysis(data=self.data)

    def publish(self):
        pass
