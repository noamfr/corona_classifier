from data_operations.data_frame_printer import Data_Frame_Printer

from analysis.analysis import Analysis
from config.config import Config


class File_Saver:
    def __init__(self, analysis: Analysis):
        self.__report_tables = analysis.get_report_tables

        self.__save_all_outputs_to_file()

    def __save_all_outputs_to_file(self):
        self.__save_report_tables_to_file()
        self.__save_graphs_to_file()

    def __save_report_tables_to_file(self):
        df_printer = Data_Frame_Printer(path=Config.DATA_ANALYSIS_OUTPUTS_PATH)

        for table_name in self.__report_tables:
            df_printer.print_df_from_dict(default_dict=self.__report_tables[table_name],
                                          file_name=table_name)

    def __save_graphs_to_file(self):
        pass
