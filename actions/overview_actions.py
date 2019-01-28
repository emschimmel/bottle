import pandas

from model.ad_object import AdObject
from model.data_frame_object import DataFrameObject
from model.tenant_enum import TenantConfig
from model.state_config import State


class OverviewActions(DataFrameObject):

    @staticmethod
    def __ad_id_overview(dataframe=DataFrameObject.uploaded_csv_data, search_string=""):
        try:
            if search_string is not "":
                return list(dataframe[dataframe['ad_id'].str.contains(search_string)]['ad_id'].unique())
            else:
                return list(dataframe['ad_id'].unique())
        except:
            return list()

    @classmethod
    def ad_id_overview(self, search_string, filter_string, offline_mode):
        if offline_mode:
            combined = DataFrameObject.uploaded_csv_data.merge(DataFrameObject.enriched_data, left_on='ad_id', right_on='ad_id', how='inner')
            ad_id_list = [id for id in self.__ad_id_overview(combined, search_string=search_string) if not DataFrameObject.enriched_data.loc[DataFrameObject.enriched_data['ad_id'] == id].empty]
        else:
            ad_id_list = self.__ad_id_overview(DataFrameObject.uploaded_csv_data, search_string=search_string)
        if filter_string:
            filtered_list = set()
            recommendations = list(DataFrameObject.enriched_data[DataFrameObject.enriched_data['title'].str.contains(filter_string)]['ad_id'].unique())
            for recommendation_id in recommendations:
                if not DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['ad_id'] == recommendation_id].empty:
                    filtered_list.add(recommendation_id)
                elif not DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['recommended_ad_id'] == recommendation_id].empty:
                    filtered_list.update(list(DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['recommended_ad_id'] == recommendation_id]['ad_id']))
            ad_id_list = list(item for item in filtered_list if item in ad_id_list)
        return ad_id_list

    @classmethod
    def get_ad_by_id(self, ad_id):
        result = AdObject()
        result.id = ad_id
        enriched_result, loaded = self.__set_enriched_data(ad_id, result)
        result = enriched_result
        if not loaded and not State.offline_mode:
            data = TenantConfig().startForId(tenant=State.tenant, id=ad_id)
            if data is not None:
                if data.loaded:
                    panda_row = pandas.DataFrame(data=[data.enriched_panda_row()], columns=DataFrameObject.enriched_data.columns)
                    DataFrameObject.enriched_data = DataFrameObject.enriched_data.append(panda_row, ignore_index=True)
                    DataFrameObject.save_enriched_data()
                    result, loaded = self.__set_enriched_data(ad_id, result)
        return result

    @classmethod
    def get_recommenders_for_initial_view(self, ad_id, limit=6):
        result_list = self.__get_recommenders_by_parent_id(ad_id)
        ad_ids_to_load = []
        if not limit:
            limit = len(result_list)
        for index, result in enumerate(result_list[0:limit]):
            result, loaded = self.__set_enriched_data(result.id, result)
            if loaded:
                result_list[index] = result
            else:
                ad_ids_to_load.append(result.id)

        return result_list, ad_ids_to_load

    @classmethod
    def __get_recommenders_by_parent_id(self, ad_id):
        # ad_object
        result_list = []
        for row in DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['ad_id'] == ad_id].values:
            result = AdObject()
            result.set_initial_data(row[1], row[2], row[3])
            result_list.append(result)
        return result_list

    @staticmethod
    def __set_enriched_data(ad_id, result):
        enriched_result = DataFrameObject.enriched_data.loc[DataFrameObject.enriched_data['ad_id'] == ad_id]
        if not enriched_result.empty:
            for row in enriched_result.values:
                result.set_enriched_data(url=row[1],
                                         img_url=row[2],
                                         title=row[3],
                                         price=row[4],
                                         location=row[5],
                                         categories=row[6],
                                         loaded=row[7],
                                         error=row[8],
                                         expired=row[9],
                                         enriched_at=row[10])
                break
        return result, not enriched_result.empty

    @staticmethod
    def reload(ad_id):
        recommenders = list(DataFrameObject.uploaded_csv_data[DataFrameObject.uploaded_csv_data['ad_id'] == ad_id]['recommended_ad_id'].unique())
        for recommender_id in recommenders:
            DataFrameObject.enriched_data = DataFrameObject.enriched_data[DataFrameObject.enriched_data['ad_id'] != recommender_id]
        DataFrameObject.enriched_data = DataFrameObject.enriched_data[DataFrameObject.enriched_data['ad_id'] != ad_id]


