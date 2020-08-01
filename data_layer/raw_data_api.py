import pandas as pd
from os import listdir, path
from configuration.config import Config


class Raw_Data_Api:
    def __init__(self):
        self.data_dict: dict
        self.raw_df: pd.DataFrame

    def get_raw_data(self):
        self.__load_raw_data_files()
        self.__mark_source_df_on_data_frames()
        self.__join_data_frames()
        return self.raw_df

    def __load_raw_data_files(self):
        file_path = Config.RAW_DATA_PATH
        dfs_dict = {}

        for data_file in listdir(file_path):
            df = pd.read_csv(path.join(file_path, data_file))
            dfs_dict[data_file] = df
        self.dfs_dict = dfs_dict

    def __mark_source_df_on_data_frames(self):
        for df_name, df in self.dfs_dict.items():
            df['source_df'] = df_name

    def __join_data_frames(self):
        df_list = []

        for df in self.dfs_dict:
            df_list.append(self.dfs_dict[df])

        self.raw_df = pd.concat(df_list)
