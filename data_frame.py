import pandas

from model.ad_object import AdObject
from model.tenant_enum import TenantConfig
import pickle
from model.config_object import FileName


class ParseCsv():
    uploaded_csv_data = pandas.DataFrame()
    enriched_data = dict()
    # enriched_data = pandas.DataFrame()

    def restore(self, file_name):
        self.uploaded_csv_data = pandas.read_csv(file_name, dtype={'ad_id':str})
        self.uploaded_csv_data = self.uploaded_csv_data.drop_duplicates()

    def save_data(self, file_name):
        self.uploaded_csv_data.to_csv(file_name)

    def amount_adds(self):
        return len(self.uploaded_csv_data['ad_id'].unique())+len(self.uploaded_csv_data['recommended_ad_id'].unique())

    def amount_enriched(self):
        return len(self.enriched_data)

    def overview_data(self):
        return self.uploaded_csv_data

    def ad_id_overview(self, search_string):
        try:
            if search_string is not "":
                return list(self.uploaded_csv_data['ad_id'].filter(like=search_string, axis='ad_id').unique())
            else:
                return list(self.uploaded_csv_data['ad_id'].unique())
        except:
            return list()

    def get_ad_by_id(self, tenant, ad_id):
        result = AdObject()
        result.id = ad_id
        if ad_id in self.enriched_data:
            enriched_result = self.enriched_data[ad_id]
            print("enriched_result {}".format(enriched_result))
            result.set_enriched_data(url=enriched_result.url,
                                     img_url=enriched_result.img_url,
                                     title=enriched_result.title,
                                     price=enriched_result.price,
                                     loaded=enriched_result.loaded,
                                     error=enriched_result.error)
        else:
            self.enriched_data_for_id(tenant=tenant, ad_id=ad_id)
            print("result ready")
        return result

    def get_recommenders_by_parent_id(self, tenant, ad_id):
        # ad_object
        result_list = []
        for row in self.uploaded_csv_data.loc[self.uploaded_csv_data['ad_id'] == ad_id].itertuples():
            result = AdObject()
            result.set_initial_data(row[2], row[3], row[4])
            if row[2] in self.enriched_data:
                enriched_result = self.enriched_data[row[2]]
                print("enriched_result {}".format(enriched_result))
                result.set_enriched_data(url=enriched_result.url,
                                         img_url=enriched_result.img_url,
                                         title=enriched_result.title,
                                         price=enriched_result.price,
                                         loaded=enriched_result.loaded,
                                         error=enriched_result.error)
            else:
                # todo: move this to a non blocking thread
                self.enriched_data_for_id(tenant=tenant, ad_id=row[2])
            result_list.append(result)
        return result_list

    def enriched_data_for_id(self, tenant, ad_id):
        data = TenantConfig().startForId(tenant=tenant, id=ad_id)
        print(data)
        if data is not None:
            if data.loaded:
                self.enriched_data.update({ad_id: data})
            self.save_enriched_data()

    def load_enriched_data(self):
        with open(FileName.dump_file_name(), 'rb') as f:
            self.enriched_data = pickle.load(f)

    def save_enriched_data(self):
        with open(FileName.dump_file_name(), 'wb') as f:
            pickle.dump(self.enriched_data, f, protocol=pickle.HIGHEST_PROTOCOL)

    # def load_config_data(self):
    #     with open(self.FILE_NAME_STATE, 'rb') as f:
    #         self.enriched_data = pickle.load(f)
    #     pass
    #
    # def save_config_data(self):
    #     with open(self.FILE_NAME_STATE, 'wb') as f:
    #         pickle.dump(self.enriched_data, f, protocol=pickle.HIGHEST_PROTOCOL)