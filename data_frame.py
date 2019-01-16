import concurrent
from concurrent.futures import ThreadPoolExecutor

import pandas

from model.ad_object import AdObject
from model.tenant_enum import TenantConfig
import pickle
from model.state_config import FileName, State


class DataFrameObject():

    uploaded_csv_data = pandas.DataFrame()
    enriched_data = dict()
    # enriched_data = pandas.DataFrame()


class DataActions(DataFrameObject):

    ############################################
    # used by overview screen
    ############################################
    @staticmethod
    def __ad_id_overview(search_string=""):
        try:
            if search_string is not "":
                return list(DataFrameObject.uploaded_csv_data[DataFrameObject.uploaded_csv_data['ad_id'].str.contains(search_string)]['ad_id'].unique())
            else:
                return list(DataFrameObject.uploaded_csv_data['ad_id'].unique())
        except:
            return list()

    @classmethod
    def ad_id_overview(self, search_string, offline_mode):
        if offline_mode:
            return [id for id in self.__ad_id_overview(search_string=search_string) if id in DataFrameObject.enriched_data]
        else:
            return self.__ad_id_overview(search_string=search_string)

    @classmethod
    def get_ad_by_id(self, ad_id):
        result = AdObject()
        result.id = ad_id
        result = self.set_enriched_data(ad_id, result)
        return result

    @classmethod
    def get_recommenders_by_parent_id(self, ad_id):
        # ad_object
        result_list = []
        for row in DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['ad_id'] == ad_id].itertuples():
            result = AdObject()
            result.set_initial_data(row[2], row[3], row[4])
            result = self.set_enriched_data(row[2], result)
            result_list.append(result)
        return result_list

    @classmethod
    def set_enriched_data(self, ad_id, result):
        if ad_id in DataFrameObject.enriched_data:
            enriched_result = DataFrameObject.enriched_data[ad_id]
            print("enriched_result {}".format(enriched_result))
            result.set_enriched_data(url=enriched_result.url,
                                     img_url=enriched_result.img_url,
                                     title=enriched_result.title,
                                     price=enriched_result.price,
                                     loaded=enriched_result.loaded,
                                     error=enriched_result.error,
                                     expired=enriched_result.expired,
                                     categories=enriched_result.categories,
                                     enriched_at=enriched_result.enriched_at)
        elif not State.offline_mode:
            self.__enriched_data_for_id(ad_id=ad_id)
        return result

    @classmethod
    def reload(self, ad_id):
        print(DataFrameObject.enriched_data[ad_id])
        del DataFrameObject.enriched_data[ad_id]
        recommenders = list(DataFrameObject.uploaded_csv_data[DataFrameObject.uploaded_csv_data['ad_id'] == ad_id]['recommended_ad_id'].unique())
        for recommender_id in recommenders:
            del DataFrameObject.enriched_data[recommender_id]

    @classmethod
    def __enriched_data_for_id(self, ad_id):
        self.__enriched_data_for_id_without_save(ad_id=ad_id)
        self.save_enriched_data()


    ############################################
    # used by config screen
    ############################################
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

    ############################################
    # modify original csv file
    ############################################
    @classmethod
    def reduce_uploaded_csv_data(self):
        DataFrameObject.uploaded_csv_data = DataFrameObject.uploaded_csv_data[DataFrameObject.uploaded_csv_data['ad_id'] in DataFrameObject.enriched_data and DataFrameObject.uploaded_csv_data['recommended_ad_id'] in DataFrameObject.enriched_data]
        self.save_data()

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

    ############################################
    # used thread
    ############################################
    @staticmethod
    def __enriched_data_for_id_without_save(ad_id):
        data = TenantConfig().startForId(tenant=State.tenant, id=ad_id)
        if data is not None:
            if data.loaded:
                DataFrameObject.enriched_data.update({ad_id: data})

    @classmethod
    def __enriched_data_for_id_with_recommendations(self, ad_id):
        self.__enriched_data_for_id_without_save(ad_id=ad_id)
        for row in DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['ad_id'] == ad_id].itertuples():
            if row[2] not in DataFrameObject.enriched_data:
                self.__enriched_data_for_id_without_save(ad_id=row[2])
        self.save_enriched_data()

    @classmethod
    def start_for_criteria(self, amount, start, end):
        all_ids = [id for id in list(DataFrameObject.uploaded_csv_data['ad_id'].unique()) if id not in DataFrameObject.enriched_data]
        if start or end:
            if not start:
                start = True
            if not end:
                end = True
            all_ids = [id for id in all_ids if id >= start and id <= end]
        if not amount:
            amount = len(all_ids)
        with concurrent.futures.ThreadPoolExecutor(max_workers=State.MAX_WORKERS) as executor:
            a = {executor.submit(self.__enriched_data_for_id_with_recommendations, id): id for id in all_ids[:int(amount)]}

    @classmethod
    def start_all(self):
        all_ids = DataFrameObject.uploaded_csv_data['ad_id'].unique()
        with concurrent.futures.ThreadPoolExecutor(max_workers=State.MAX_WORKERS) as executor:
            a = {executor.submit(self.__enriched_data_for_id_with_recommendations, id): id for id in all_ids if id not in DataFrameObject.enriched_data}

    ############################################
    # file actions
    ############################################

    @staticmethod
    def restore():
        DataFrameObject.uploaded_csv_data = pandas.read_csv(FileName.original_file_name(), dtype={'ad_id':str, 'recommended_ad_id':str})

    @staticmethod
    def save_data():
        DataFrameObject.uploaded_csv_data.to_csv(FileName.original_file_name(), index=False)
        DataFrameObject.uploaded_csv_data = pandas.read_csv(FileName.original_file_name(), dtype={'ad_id':str, 'recommended_ad_id':str})

    @staticmethod
    def load_enriched_data():
        with open(FileName.dump_file_name(), 'rb') as f:
            DataFrameObject.enriched_data = pickle.load(f)

    @staticmethod
    def save_enriched_data():
        with open(FileName.dump_file_name(), 'wb') as f:
            pickle.dump(DataFrameObject.enriched_data, f, protocol=pickle.HIGHEST_PROTOCOL)