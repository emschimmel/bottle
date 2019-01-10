import concurrent
from concurrent.futures import ThreadPoolExecutor

import pandas

from model.ad_object import AdObject
from model.tenant_enum import TenantConfig
import pickle
from model.config_object import FileName, State


class DataFrame():

    uploaded_csv_data = pandas.DataFrame()
    enriched_data = dict()
    # enriched_data = pandas.DataFrame()


class DataActions(DataFrame):

    ############################################
    # used by overview screen
    ############################################
    @staticmethod
    def ad_id_overview(search_string=""):
        try:
            if search_string is not "":
                return list(DataFrame.uploaded_csv_data['ad_id'].filter(like=search_string, axis='ad_id').unique())
            else:
                return list(DataFrame.uploaded_csv_data['ad_id'].unique())
        except:
            return list()

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
        for row in DataFrame.uploaded_csv_data.loc[DataFrame.uploaded_csv_data['ad_id'] == ad_id].itertuples():
            result = AdObject()
            result.set_initial_data(row[2], row[3], row[4])
            result = self.set_enriched_data(row[2], result)
            result_list.append(result)
        return result_list

    @classmethod
    def set_enriched_data(self, ad_id, result):
        if ad_id in DataFrame.enriched_data:
            enriched_result = DataFrame.enriched_data[ad_id]
            print("enriched_result {}".format(enriched_result))
            result.set_enriched_data(url=enriched_result.url,
                                     img_url=enriched_result.img_url,
                                     title=enriched_result.title,
                                     price=enriched_result.price,
                                     loaded=enriched_result.loaded,
                                     error=enriched_result.error)
        elif not State.offline_mode:
            self.__enriched_data_for_id(ad_id=ad_id)
        return result

    @classmethod
    def __enriched_data_for_id(self, ad_id):
        self.__enriched_data_for_id_without_save(ad_id=ad_id)
        self.save_enriched_data()


    ############################################
    # used by config screen
    ############################################
    @staticmethod
    def amount_adds():
        return len(DataFrame.uploaded_csv_data['ad_id'].unique())

    @staticmethod
    def amount_enriched():
        count = 0
        all = DataFrame.uploaded_csv_data['ad_id'].unique()
        for id in all:
            if id in DataFrame.enriched_data:
                count += 1
        return count

    ############################################
    # modify original csv file
    ############################################
    @classmethod
    def reduce_uploaded_csv_data(self):
        parent_ids = DataFrame.uploaded_csv_data['ad_id'].unique()
        for id in parent_ids:
            if id not in DataFrame.enriched_data:
                DataFrame.uploaded_csv_data = DataFrame.uploaded_csv_data[DataFrame.uploaded_csv_data['ad_id'] != id]
        recommendation_ids = DataFrame.uploaded_csv_data['recommended_ad_id'].unique()
        for id in recommendation_ids:
            if id not in DataFrame.enriched_data:
                DataFrame.uploaded_csv_data = DataFrame.uploaded_csv_data[DataFrame.uploaded_csv_data['recommended_ad_id'] != id]
        self.save_data()

    ############################################
    # used thread
    ############################################
    @staticmethod
    def __enriched_data_for_id_without_save(ad_id):
        data = TenantConfig().startForId(tenant=State.tenant, id=ad_id)
        if data is not None:
            if data.loaded:
                DataFrame.enriched_data.update({ad_id: data})

    @classmethod
    def __enriched_data_for_id_with_recommendations(self, ad_id):
        self.__enriched_data_for_id_without_save(ad_id=ad_id)
        for row in DataFrame.uploaded_csv_data.loc[DataFrame.uploaded_csv_data['ad_id'] == ad_id].itertuples():
            if row[2] not in DataFrame.enriched_data:
                self.__enriched_data_for_id_without_save(ad_id=row[2])
        self.save_enriched_data()

    @classmethod
    def start_for_criteria(self, amount, start, end):
        all_ids = [id for id in list(DataFrame.uploaded_csv_data['ad_id'].unique()) if id not in DataFrame.enriched_data]
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
        all_ids = DataFrame.uploaded_csv_data['ad_id'].unique()
        with concurrent.futures.ThreadPoolExecutor(max_workers=State.MAX_WORKERS) as executor:
            a = {executor.submit(self.__enriched_data_for_id_with_recommendations, id): id for id in all_ids if id not in DataFrame.enriched_data}

    ############################################
    # file actions
    ############################################

    @staticmethod
    def restore():
        DataFrame.uploaded_csv_data = pandas.read_csv(FileName.original_file_name(), dtype={'ad_id':str})
        DataFrame.uploaded_csv_data = DataFrame.uploaded_csv_data.drop_duplicates()

    @staticmethod
    def save_data():
        DataFrame.uploaded_csv_data.to_csv(FileName.original_file_name())

    @staticmethod
    def load_enriched_data():
        with open(FileName.dump_file_name(), 'rb') as f:
            DataFrame.enriched_data = pickle.load(f)

    @staticmethod
    def save_enriched_data():
        with open(FileName.dump_file_name(), 'wb') as f:
            pickle.dump(DataFrame.enriched_data, f, protocol=pickle.HIGHEST_PROTOCOL)