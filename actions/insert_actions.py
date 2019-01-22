import pandas

from model.data_frame_object import DataFrameObject


class InsertActions(DataFrameObject):

    @classmethod
    def insert_single_row(self, ad_id, recommendation_list):
        for item in recommendation_list:
            row = [ad_id, item.id, item.rank, int(item.score)]
            # DataFrame.uploaded_csv_data.append(pandas.DataFrame([row], columns=DataFrame.uploaded_csv_data.columns))
            DataFrameObject.uploaded_csv_data.append(pandas.DataFrame([row], columns=DataFrameObject.uploaded_csv_data.columns))
        self.save_data()

    @classmethod
    def insert_multi_row(self, raw_collection):
        for row_item in raw_collection:
            row = row_item.split(',')
            DataFrameObject.uploaded_csv_data.append(pandas.DataFrame([row], columns=DataFrameObject.uploaded_csv_data.columns))
        self.save_data()