from data.data import Data
from analysis.analysis import Analysis
from publish.file_saver import File_Saver


class Pipeline:
    def __init__(self):
        self.data: Data or None = None
        self.analysis: Analysis or None = None
        self.file_saver: File_Saver or None = None

    def get_data(self):
        self.data = Data(remove_missing_values=True)

    def run_analysis(self):
        self.analysis = Analysis(data=self.data)

    def save_outputs_to_file(self):
        self.file_saver = File_Saver(analysis=self.analysis)
