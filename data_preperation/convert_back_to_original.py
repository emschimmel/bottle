import pandas


class EnrichOutputData():

    meta_data = "meta_data.csv"
    model_output = "export_for_user.csv"

    def enrich(self):
        meta_rows = pandas.read_csv(self.meta_data, dtype={'combined_key':str})
        model = pandas.read_csv(self.model_output, dtype={'ad_id':str, 'recommended_ad_id':str})
        rows = []
        for item in model.iterrows():
            lot_id = item[1][1]
            print(lot_id)
            combined_keys = meta_rows[meta_rows['combined_key'].str.contains(lot_id, na=False)]['combined_key'].unique()
            if len(combined_keys):
                combined_key = combined_keys[0]
            else:
                combined_key = lot_id
            rows.append([item[1][0], combined_key, item[1][2], item[1][3]])
        original_csv_data = pandas.DataFrame(rows, columns=['ad_id', 'recommended_ad_id', 'rank', 'score'])
        original_csv_data.to_csv('../config/original.csv', index=False)


if __name__ == '__main__':
    EnrichOutputData().enrich()