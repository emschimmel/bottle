import pandas

from model.data_frame_object import DataFrameObject


class ConfigActions(DataFrameObject):
    @staticmethod
    def amount_adds():
        try:
            return len(DataFrameObject.uploaded_csv_data['ad_id'].unique())
        except:
            return 0

    @staticmethod
    def amount_enriched():
        count = 0
        try:
            all = DataFrameObject.uploaded_csv_data['ad_id'].unique()
            for id in all:
                if id in DataFrameObject.enriched_data:
                    count += 1
        except:
            pass
        return count

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
