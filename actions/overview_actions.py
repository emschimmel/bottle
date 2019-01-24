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

    @staticmethod
    def set_enriched_data(ad_id, result):
        enriched_result = DataFrameObject.enriched_data.loc[DataFrameObject.enriched_data['ad_id'] == ad_id]
        if not enriched_result.empty:
            for row in enriched_result.itertuples():
                result.set_enriched_data(url=row[2],
                                         img_url=row[3],
                                         title=row[4],
                                         price=row[5],
                                         location=row[6],
                                         categories=row[7],
                                         loaded=row[8],
                                         error=row[9],
                                         expired=row[10],
                                         enriched_at=row[11],
                )
                break
        elif not State.offline_mode:
            print("Retrieving data for ad id {id}".format(id=ad_id))
            data = TenantConfig().startForId(tenant=State.tenant, id=ad_id)
            if data is not None:
                if data.loaded:
                    panda_row = pandas.DataFrame(data=[data.enriched_panda_row()], columns=DataFrameObject.enriched_data.columns)
                    DataFrameObject.enriched_data = DataFrameObject.enriched_data.append(panda_row, ignore_index=True)
            DataFrameObject.save_enriched_data()
        return result

    @staticmethod
    def reload(ad_id):
        recommenders = list(DataFrameObject.uploaded_csv_data[DataFrameObject.uploaded_csv_data['ad_id'] == ad_id]['recommended_ad_id'].unique())
        for recommender_id in recommenders:
            DataFrameObject.enriched_data = DataFrameObject.enriched_data[DataFrameObject.enriched_data['ad_id'] != recommender_id]
        DataFrameObject.enriched_data = DataFrameObject.enriched_data[DataFrameObject.enriched_data['ad_id'] != ad_id]


