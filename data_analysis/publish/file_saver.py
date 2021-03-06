from analysis_operations.graph_functions import bar_chart, histogram

from data_operations.data_frame_printer import Data_Frame_Printer

from analysis.analysis import Analysis
from config.data_analysis_config import Data_Analysis_Config


class File_Saver:
    def __init__(self, analysis: Analysis):
        self.analysis = analysis
        self.__report_tables = self.analysis.report_tables
        self.__graph_vectors = self.analysis.graph_vectors

        self.__save_all_outputs_to_file()

    def __save_all_outputs_to_file(self):
        self.__save_report_tables_to_file()
        self.__save_graphs_to_file()

    def __save_report_tables_to_file(self):
        df_printer = Data_Frame_Printer(path=Data_Analysis_Config.DATA_ANALYSIS_OUTPUTS_PATH)

        for table_name in self.__report_tables:
            df_printer.print_df_from_dict(default_dict=self.__report_tables[table_name],
                                          file_name=table_name)

    def __save_graphs_to_file(self):

        bar_chart(x=self.__report_tables['source_files_missing_values_analysis']['source_file'],
                  height=self.__report_tables['source_files_missing_values_analysis']['missing_values_percent'],
                  title='Source_files_missing_values_%',
                  x_label='source_files',
                  y_label='missing_values_%',
                  path=Data_Analysis_Config.DATA_ANALYSIS_OUTPUTS_PATH)

        bar_chart(x=self.__report_tables['data_field_missing_values_analysis']['data_field'],
                  height=self.__report_tables['data_field_missing_values_analysis']['missing_data_percent'],
                  title='Data_fields_missing_values_%',
                  x_label='Data_fields',
                  y_label='missing_values_%',
                  path=Data_Analysis_Config.DATA_ANALYSIS_OUTPUTS_PATH)

        vector = self.__graph_vectors['patient_missing_values']
        histogram(path=Data_Analysis_Config.DATA_ANALYSIS_OUTPUTS_PATH,
                  vector=vector,
                  label='patient_missing_values',
                  x_label='missing_values',
                  y_label='count',
                  bins=vector.max(),
                  x_ticks=range(0, vector.max() + 2, 2),
                  add_mean_line=True)

        for analysis_vector in self.__graph_vectors['continuous_vectors']:
            histogram(path=Data_Analysis_Config.DATA_ANALYSIS_OUTPUTS_PATH,
                      vector=analysis_vector.vector_without_missing_values,
                      label=analysis_vector.field_name,
                      x_label=analysis_vector.field_name,
                      y_label='count',
                      bins=50,
                      x_ticks=range(0, int(analysis_vector.vector_without_missing_values.max()) + 2, 2),
                      add_mean_line=True)
