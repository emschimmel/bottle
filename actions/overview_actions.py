from model.ad_object import AdObject
from model.data_frame_object import DataFrameObject
from model.tenant_enum import TenantConfig
from model.state_config import State


class OverviewActions(DataFrameObject):

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
    def ad_id_overview(self, search_string, filter_string, offline_mode):
        if offline_mode:
            ad_id_list = [id for id in self.__ad_id_overview(search_string=search_string) if id in DataFrameObject.enriched_data]
        else:
            ad_id_list = self.__ad_id_overview(search_string=search_string)
        if filter_string:
            print(filter_string)
            ad_id_list = [id for id in ad_id_list if id in DataFrameObject.enriched_data and filter_string in DataFrameObject.enriched_data[id].title]
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
        if ad_id in DataFrameObject.enriched_data:
            enriched_result = DataFrameObject.enriched_data[ad_id]
            # print("enriched_result {}".format(enriched_result))
            result.set_enriched_data(url=enriched_result.url,
                                     img_url=enriched_result.img_url,
                                     title=enriched_result.title,
                                     price=enriched_result.price,
                                     loaded=enriched_result.loaded,
                                     error=enriched_result.error,
                                     expired=enriched_result.expired,
                                     categories=enriched_result.categories,
                                     enriched_at=enriched_result.enriched_at,
                                     location=enriched_result.location)
        elif not State.offline_mode:
            print("Retrieving data for ad id {id}".format(id=ad_id))
            data = TenantConfig().startForId(tenant=State.tenant, id=ad_id)
            if data is not None:
                if data.loaded:
                    DataFrameObject.enriched_data.update({ad_id: data})
            DataFrameObject.save_enriched_data()
        return result

    @staticmethod
    def reload(ad_id):
        print(DataFrameObject.enriched_data[ad_id])
        del DataFrameObject.enriched_data[ad_id]
        recommenders = list(DataFrameObject.uploaded_csv_data[DataFrameObject.uploaded_csv_data['ad_id'] == ad_id]['recommended_ad_id'].unique())
        for recommender_id in recommenders:
            del DataFrameObject.enriched_data[recommender_id]

