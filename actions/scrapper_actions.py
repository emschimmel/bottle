import pandas

from model.data_frame_object import DataFrameObject

from multiprocessing import Pool

from model.state_config import State
from model.tenant_enum import TenantConfig


def start_enrich_process(ad_id):
    print("starting {ad_id}".format(ad_id=ad_id))
    return TenantConfig().startForId(tenant=State.tenant, id=ad_id)


def callback_enrich_process(data):
    print("saving {amount}".format(amount=len(data)))
    panda_items = list()
    for item in data:
        if item.loaded:
            row = item.enriched_panda_row()
            panda_items.append(row)

    panda_row = pandas.DataFrame(data=panda_items, columns=DataFrameObject.enriched_data.columns)
    DataFrameObject.enriched_data = DataFrameObject.enriched_data.append(panda_row, ignore_index=True)

    ScrapperActions.save_enriched_data()


class ScrapperActions(DataFrameObject):

    pool = Pool(State.MAX_WORKERS)

    @staticmethod
    def amount_adds():
        try:
            return len(DataFrameObject.uploaded_csv_data['ad_id'].unique())
        except:
            return 0

    @staticmethod
    def amount_enriched():
        try:
            return len(DataFrameObject.enriched_data['ad_id'].isin(DataFrameObject.uploaded_csv_data['ad_id']))
        except:
            return 0

    @staticmethod
    def amount_adds_for_list():
        try:
            return len(DataFrameObject.uploaded_add_list_data['ad_id'].unique())
        except:
            return 0

    @staticmethod
    def amount_enriched_for_list():
        try:
            return len(DataFrameObject.enriched_data['ad_id'].isin(DataFrameObject.uploaded_add_list_data['ad_id']))
        except:
            return 0

    @classmethod
    def start_for_criteria(self, amount, start, end):
        all_ids = [id for id in list(DataFrameObject.uploaded_csv_data['ad_id'].unique()) if
                   id not in DataFrameObject.enriched_data]
        if start or end:
            if not start:
                start = True
            if not end:
                end = True
            all_ids = [id for id in all_ids if id >= start and id <= end]
        if amount:
            all_ids = all_ids[:int(amount)]

        self.__start_processes_for_list_and_recommenders(all_ids)

    @classmethod
    def start_all(self):
        all_ids = DataFrameObject.uploaded_csv_data.loc[~DataFrameObject.uploaded_csv_data['ad_id'].isin(DataFrameObject.enriched_data['ad_id']) == False]['ad_id']
        self.__start_processes_for_list_and_recommenders(all_ids)

    @classmethod
    def start_for_criteria_for_list(self, amount, start, end):
        all_ids = [id for id in list(DataFrameObject.uploaded_add_list_data['ad_id'].unique()) if
                   id not in DataFrameObject.enriched_data]
        if start or end:
            if not start:
                start = True
            if not end:
                end = True
            all_ids = [id for id in all_ids if id >= start and id <= end]
        if amount:
            all_ids = all_ids[:int(amount)]

        self.__start_processes_for_list_without_recommenders(all_ids)

    @classmethod
    def start_all_for_list(self):
        all_ids = DataFrameObject.uploaded_add_list_data.loc[DataFrameObject.uploaded_add_list_data['ad_id'].isin(DataFrameObject.enriched_data['ad_id']) == False]['ad_id']
        self.__start_processes_for_list_without_recommenders(all_ids)

    @classmethod
    def __start_processes_for_list_without_recommenders(self, all_ids):
        for i in range(0, len(all_ids), State.SAVE_INTERVAL):
            print("processing {amount} before saving".format(amount=str(len(all_ids[i:i + State.SAVE_INTERVAL]))))
            self.start_processes_for_list(all_ids[i:i + State.SAVE_INTERVAL])

    @classmethod
    def __start_processes_for_list_and_recommenders(self, all_ids):
        for i in range(0, len(all_ids), State.SAVE_INTERVAL):
            chunk_with_recommenders = list()
            for ad_id in all_ids[i:i + State.SAVE_INTERVAL]:
                chunk_with_recommenders.append(ad_id)
                chunk_with_recommenders.extend([row[1] for row in DataFrameObject.uploaded_csv_data.loc[
                    DataFrameObject.uploaded_csv_data['ad_id'] == ad_id].values if
                                                row[1] not in DataFrameObject.enriched_data])
            print("processing {amount} before saving".format(amount=str(len(chunk_with_recommenders))))
            self.start_processes_for_list(chunk_with_recommenders)

    @classmethod
    def start_processes_for_list(self, all_ids):
        self.pool.map_async(func=start_enrich_process,
                       iterable=all_ids,
                       chunksize=10,
                       callback=callback_enrich_process)
