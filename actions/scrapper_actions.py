from model.data_frame_object import DataFrameObject

from multiprocessing import Pool

from model.state_config import State
from model.tenant_enum import TenantConfig


def start_enrich_process(ad_id):
    return TenantConfig().startForId(tenant=State.tenant, id=ad_id)


def callback_enrich_process(data):
    for item in data:
        if item.loaded:
            ScrapperActions.enriched_data.update({item.id: item})
    ScrapperActions.save_enriched_data()


class ScrapperActions(DataFrameObject):

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

        self.__start_processes_for_list(all_ids)

    @classmethod
    def start_all(self):
        all_ids = DataFrameObject.uploaded_csv_data['ad_id'].unique()
        all_ids = [id for id in all_ids if id not in DataFrameObject.enriched_data]
        self.__start_processes_for_list(all_ids)

    @staticmethod
    def __start_processes_for_list(all_ids):
        pool = Pool(State.MAX_WORKERS)
        for i in range(0, len(all_ids), State.SAVE_INTERVAL):
            chunk_with_recommenders = list()
            for ad_id in all_ids[i:i + State.SAVE_INTERVAL]:
                chunk_with_recommenders.append(ad_id)
                chunk_with_recommenders.extend([row[2] for row in DataFrameObject.uploaded_csv_data.loc[
                    DataFrameObject.uploaded_csv_data['ad_id'] == ad_id].itertuples() if
                                                row[2] not in DataFrameObject.enriched_data])
            print("processing {amount} before saving".format(amount=str(len(chunk_with_recommenders))))
            pool.map_async(func=start_enrich_process,
                                chunksize=10,
                                iterable=chunk_with_recommenders,
                                callback=callback_enrich_process)
        pool.terminate()
        pool.join()
        pool.close()

