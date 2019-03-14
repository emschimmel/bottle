from espandas import Espandas

from model.data_frame_object import DataFrameObject
from model.state_config import State


class ElasticActions(DataFrameObject):

    @classmethod
    def start_import(self):
        self.import_enriched_data(DataFrameObject.enriched_data, "enriched_data")
        self.import_enriched_data(DataFrameObject.uploaded_csv_data, "uploaded_csv_data")
        self.import_enriched_data(DataFrameObject.uploaded_add_list_data, "uploaded_add_list_data")

    @staticmethod
    def import_enriched_data(data, type, index=State.tenant):
        elastic_hosts = ["http://{ip}:{port}/".format(ip=State.ELASTIC_IP, port=State.ELASTIC_PORT)]
        esp = Espandas(hosts=elastic_hosts, verify_certs=True)
        esp.es_write(data, index, type)