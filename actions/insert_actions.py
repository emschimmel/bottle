import pandas

from model.data_frame_object import DataFrameObject


class InsertActions(DataFrameObject):

    @staticmethod
    def insert_single_row_with_recommendations(ad_id, recommendation_list):
        for item in recommendation_list:
            panda_row = pandas.DataFrame([[ad_id, item.id, item.rank, int(item.score)]], columns=DataFrameObject.uploaded_csv_data.columns)
            DataFrameObject.uploaded_csv_data = DataFrameObject.uploaded_csv_data.append(panda_row, ignore_index=True)
        DataFrameObject.save_data()

    @staticmethod
    def insert_multi_row_with_recommendations(raw_collection):
        for row_item in raw_collection:
            row = row_item.split(',')
            DataFrameObject.uploaded_csv_data = DataFrameObject.uploaded_csv_data.append(pandas.DataFrame([row], columns=DataFrameObject.uploaded_csv_data.columns))
        DataFrameObject.save_data()

    @staticmethod
    def insert_single_row_add_list(ad_id):
        panda_row = pandas.DataFrame([[ad_id]], columns=DataFrameObject.uploaded_add_list_data.columns)
        DataFrameObject.uploaded_add_list_data = DataFrameObject.uploaded_add_list_data.append(panda_row, ignore_index=True)
        DataFrameObject.save_add_list_data()

    @staticmethod
    def insert_multi_row_add_list(raw_collection):
        for row_item in raw_collection:
            panda_row = pandas.DataFrame([[row_item]], columns=DataFrameObject.uploaded_add_list_data.columns)
            DataFrameObject.uploaded_add_list_data = DataFrameObject.uploaded_add_list_data.append(panda_row, ignore_index=True)
        DataFrameObject.save_add_list_data()

    @staticmethod
    def insert_single_row_user_recommendations(ad_id, recommendation_list):
        for item in recommendation_list:
            # todo: match form and fields
            panda_row = pandas.DataFrame([[ad_id, item.id, item.rank, int(item.score)]], columns=DataFrameObject.uploaded_user_recom_data.columns)
            DataFrameObject.uploaded_user_recom_data = DataFrameObject.uploaded_user_recom_data.append(panda_row, ignore_index=True)
        DataFrameObject.save_user_recom_data()

    @staticmethod
    def insert_multi_row_user_recom_list(raw_collection):
        for row_item in raw_collection:
            row = row_item.split(',')
            DataFrameObject.uploaded_user_recom_data = DataFrameObject.uploaded_user_recom_data.append(
                pandas.DataFrame([row], columns=DataFrameObject.uploaded_user_recom_data.columns))
        DataFrameObject.save_user_recom_data()

    @staticmethod
    def insert_single_row_product_recommendations(ad_id, recommendation_list):
        for item in recommendation_list:
            # todo: match form and fields
            panda_row = pandas.DataFrame([[ad_id, item.id, item.rank, int(item.score)]], columns=DataFrameObject.uploaded_product_recom_data.columns)
            DataFrameObject.uploaded_product_recom_data = DataFrameObject.uploaded_product_recom_data.append(panda_row, ignore_index=True)
        DataFrameObject.save_product_recom_data()


    @staticmethod
    def insert_multi_row_product_recom_list(raw_collection):
        for row_item in raw_collection:
            row = row_item.split(',')
            DataFrameObject.uploaded_product_recom_data = DataFrameObject.uploaded_product_recom_data.append(
                pandas.DataFrame([row], columns=DataFrameObject.uploaded_product_recom_data.columns))
        DataFrameObject.save_product_recom_data()
