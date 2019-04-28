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

    @staticmethod
    def __ad_id_overview_user_recom(dataframe=DataFrameObject.uploaded_csv_data, search_string=""):
        try:
            if search_string is not "":
                return list(dataframe[dataframe['lot_id'].str.contains(search_string)]['lot_id'].unique())
            else:
                return list(dataframe['lot_id'].unique())
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
            recommendations = list(DataFrameObject.enriched_data[DataFrameObject.enriched_data['title'].notnull()&DataFrameObject.enriched_data['title'].str.contains(filter_string)]['ad_id'].unique())
            for recommendation_id in recommendations:
                if not DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['ad_id'] == recommendation_id].empty:
                    filtered_list.add(recommendation_id)
                elif not DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['recommended_ad_id'] == recommendation_id].empty:
                    filtered_list.update(list(DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['recommended_ad_id'] == recommendation_id]['ad_id']))
            ad_id_list = list(item for item in filtered_list if item in ad_id_list)
        return ad_id_list

    @classmethod
    def ad_id_overview_user_recom(self, search_string, filter_string, offline_mode):
        if offline_mode:
            ad_id_list = [id for id in DataFrameObject.uploaded_product_recom_data['lot_id'].unique() if not DataFrameObject.enriched_data.loc[DataFrameObject.enriched_data['ad_id'] == str(id)].empty]
        else:
            ad_id_list = self.__ad_id_overview_user_recom(DataFrameObject.uploaded_product_recom_data, search_string=search_string)
        if filter_string:
            filtered_list = set()
            recommendations = list(DataFrameObject.enriched_data[DataFrameObject.enriched_data['title'].notnull()&DataFrameObject.enriched_data['title'].str.contains(filter_string)]['ad_id'].unique())
            for recommendation_id in recommendations:
                if not DataFrameObject.uploaded_product_recom_data.loc[DataFrameObject.uploaded_product_recom_data['lot_id'] == recommendation_id].empty:
                    filtered_list.add(recommendation_id)
                elif not DataFrameObject.uploaded_product_recom_data.loc[DataFrameObject.uploaded_product_recom_data['lot_id'] == recommendation_id].empty:
                    filtered_list.update(list(DataFrameObject.uploaded_product_recom_data.loc[DataFrameObject.uploaded_product_recom_data['lot_id'] == recommendation_id]['ad_id']))
            ad_id_list = list(item for item in filtered_list if item in ad_id_list)
        return ad_id_list

    @classmethod
    def get_ad_by_id(self, ad_id):
        result = AdObject()
        result.id = ad_id
        auction = ""
        if State.system_mode == State.AD_USER_RECOM_MODE:
            full_adds = DataFrameObject.uploaded_product_recom_data.loc[DataFrameObject.uploaded_product_recom_data['lot_id'] == int(ad_id)].values
            for row in full_adds:
                auction = row[1]
                result.title = row[3]
                result.categories = row[6]
                break
        enriched_result, loaded = self.__set_enriched_data(ad_id, result)
        result = enriched_result
        if not loaded and not State.offline_mode:
            data = TenantConfig().startForId(tenant=State.tenant, id="{auction}_{lot_id}".format(auction=auction, lot_id=ad_id))
            if data is not None:
                if data.loaded:
                    data.title = result.title
                    data.categories = [result.categories]
                    data = data.enriched_panda_row()
                    panda_row = pandas.DataFrame(data=[data], columns=DataFrameObject.enriched_data.columns)
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
    def get_product_recommenders_for_initial_view(self, ad_id, limit=6):
        result_list = self.__get_product_recommendations_by_parent_id(ad_id)
        ad_ids_to_load = []
        if not limit:
            limit = len(result_list)
        for index, result in enumerate(result_list[0:limit]):
            result, loaded = self.__set_enriched_data(result.id, result)
            if loaded:
                result_list[index] = result
            else:
                auction = DataFrameObject.uploaded_product_recom_data.loc[DataFrameObject.uploaded_product_recom_data['lot_id'] == result.id]['auction']
                if not auction.empty:
                    ad_ids_to_load.append("{auction}_{lot_id}".format(auction=auction.values[0], lot_id=result.id))
                else:
                    del result_list[index]
        return result_list, ad_ids_to_load

    def get_user_recommenders_for_initial_view(self, ad_id, user_id, limit=6):
        result_list = self.__get_user_recommendations_by_parent_id(ad_id, user_id)
        ad_ids_to_load = []
        if not limit:
            limit = len(result_list)
        for index, result in enumerate(result_list[0:limit]):
            result, loaded = self.__set_enriched_data(result.id, result)
            if loaded:
                result_list[index] = result
            else:
                auction = DataFrameObject.uploaded_product_recom_data.loc[DataFrameObject.uploaded_product_recom_data['lot_id'] == result.id]['auction']

                if not auction.empty:
                    ad_ids_to_load.append("{auction}_{lot_id}".format(auction=auction.values[0], lot_id=result.id))
                else:
                    del result_list[index]
        return result_list, ad_ids_to_load

    @classmethod
    def get_users_for_product_recommendations(self, ad_id):
        return list(DataFrameObject.uploaded_user_recom_data[DataFrameObject.uploaded_user_recom_data['lot_id']==int(ad_id)]['user'].unique())

    @classmethod
    def __get_recommenders_by_parent_id(self, ad_id):
        # ad_object
        result_list = []
        for row in DataFrameObject.uploaded_csv_data.loc[DataFrameObject.uploaded_csv_data['ad_id'] == ad_id].values:
            result = AdObject()
            result.set_initial_data(row[1], row[2], row[3])
            result_list.append(result)
        return result_list

    @classmethod
    def __get_product_recommendations_by_parent_id(self, ad_id):
        result_list = []
        for row in DataFrameObject.uploaded_product_recom_data.loc[DataFrameObject.uploaded_product_recom_data['lot_id'] == int(ad_id)].values:
            result = AdObject()
            result.set_initial_data(row[7], row[14], row[14])
            result.title = row[10]
            result.categories = row[13]
            result_list.append(result)
        return result_list

    @classmethod
    def __get_user_recommendations_by_parent_id(self, ad_id, user_id):
        #todo: do something with the category of the ad_id
        result_list = []
        for row in DataFrameObject.uploaded_user_recom_data.loc[DataFrameObject.uploaded_user_recom_data['user'] == int(user_id)].values:
            if row[1] != ad_id:
                result = AdObject()
                result.set_initial_data(row[1], row[2], row[2])
                result.title = row[7]
                result.categories = row[10]
                result_list.append(result)
        return result_list

    @staticmethod
    def __set_enriched_data(ad_id, result):
        enriched_result = DataFrameObject.enriched_data.loc[DataFrameObject.enriched_data['ad_id'] == str(ad_id)]
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
                                         enriched_at=row[10],
                                         extra_data=row[11],
                                         extra_images=row[12])
                break
        return result, not enriched_result.empty

    @staticmethod
    def reload(ad_id):
        recommenders = list(DataFrameObject.uploaded_csv_data[DataFrameObject.uploaded_csv_data['ad_id'] == ad_id]['recommended_ad_id'].unique())
        for recommender_id in recommenders:
            DataFrameObject.enriched_data = DataFrameObject.enriched_data[DataFrameObject.enriched_data['ad_id'] != recommender_id]
        DataFrameObject.enriched_data = DataFrameObject.enriched_data[DataFrameObject.enriched_data['ad_id'] != ad_id]

    @staticmethod
    def reload_list_item(ad_id):
        DataFrameObject.enriched_data = DataFrameObject.enriched_data[DataFrameObject.enriched_data['ad_id'] != ad_id]

    @classmethod
    def ad_list_for_page(self, search_string, filter_string, offline_mode, current_page, max_per_page):
        if offline_mode:
            combined = DataFrameObject.uploaded_add_list_data.merge(DataFrameObject.enriched_data, left_on='ad_id', right_on='ad_id', how='inner')
            ad_id_list = [id for id in self.__ad_id_overview(combined, search_string=search_string) if not DataFrameObject.enriched_data.loc[DataFrameObject.enriched_data['ad_id'] == id].empty]
        else:
            ad_id_list = self.__ad_id_overview(DataFrameObject.uploaded_add_list_data, search_string=search_string)
        if filter_string:
            filtered_list = set()
            ads = list(DataFrameObject.enriched_data[DataFrameObject.enriched_data['title'].notnull()&DataFrameObject.enriched_data['title'].str.contains(filter_string)]['ad_id'].unique())
            for id in ads:
                if not DataFrameObject.uploaded_add_list_data.loc[DataFrameObject.uploaded_add_list_data['ad_id'] == id].empty:
                    filtered_list.add(id)
            ad_id_list = list(item for item in filtered_list if item in ad_id_list)

        ###

        paged_output = [ad_id_list[i:i + max_per_page] for i in range(0, len(ad_id_list), max_per_page)]
        amount_pages = len(paged_output) - 1
        if current_page is None:
            current_page = 0
        print("full_output length {l}".format(l=len(ad_id_list)))
        output = []
        if len(paged_output) > 0:
            output = paged_output[current_page]

        ###
        enriched_data_to_show = list(self.get_ad_by_id(id) for id in output)
        return enriched_data_to_show, amount_pages, current_page

