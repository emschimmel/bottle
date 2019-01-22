import pandas

from model.data_frame_object import DataFrameObject


class InsertActions(DataFrameObject):

    @staticmethod
    def insert_single_row(ad_id, recommendation_list):
        for item in recommendation_list:
            panda_row = pandas.DataFrame([[ad_id, item.id, item.rank, int(item.score)]], columns=DataFrameObject.uploaded_csv_data.columns)
            DataFrameObject.uploaded_csv_data = DataFrameObject.uploaded_csv_data.append(panda_row, ignore_index=True)
        DataFrameObject.save_data()

    @staticmethod
    def insert_multi_row(raw_collection):
        for row_item in raw_collection:
            row = row_item.split(',')
            DataFrameObject.uploaded_csv_data = DataFrameObject.uploaded_csv_data.append(pandas.DataFrame([row], columns=DataFrameObject.uploaded_csv_data.columns))
        DataFrameObject.save_data()