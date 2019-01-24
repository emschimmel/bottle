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
                if not DataFrameObject.enriched_data.loc[DataFrameObject.enriched_data['id'] == id].empty:
                    count += 1
        except:
            pass
        return count

