
import pandas
# import sns as sns

raw_data = pandas.read_csv("user_data_export.csv", dtype={'user_id':str, 'domain_user_id':str, 'session_id':str, 'lot_id':int, 'rank':int})
# raw_data.assign(id=(raw_data['user_id'] + '_' + raw_data['domain_user_id'] + '_' + raw_data['session_id']).astype('category').cat.codes)
raw_data['id'] = raw_data.groupby(['user_id','domain_user_id','session_id']).ngroup()
# raw_data['user'] = raw_data.factorize(raw_data.user_id+raw_data.domain_user_id+raw_data.session_id)[0]
print(raw_data.head(5))


# user_data = pandas.DataFrame(raw_data.groupby['user_id'])
# user_data.dropna(inplace=True)

# sns.pairplot(user_data, hue='rating')

from pyspark.mllib.recommendation import ALS, MatrixFactorizationModel, Rating

data = spark.from_csv("")