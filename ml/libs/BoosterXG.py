import xgboost as xgb
from sklearn.cross_validation import train_test_split

class BoosterXG:

	def __init__(self, df_train, df_test, target, features, params, num_boost_round, early_stopping_rounds):
		self.df_train = df_train
		self.df_test = df_test
		self.target = target
		self.features = features
		self.params = params
		self.num_boost_round = num_boost_round
		self.early_stopping_rounds = early_stopping_rounds

	def run_xgboost(self, df_train=None, df_test=None, ntree_limit=None):
		if df_train == None:
			df_train = self.df_train
		if df_test == None:
			df_test = self.df_test

		target_train = df_train[self.target]
		dm_train = xgb.DMatrix(df_train[self.features], target_train)

		gbm = xgb.train(self.params, dm_train, num_boost_round=self.num_boost_round, early_stopping_rounds=self.early_stopping_rounds)
		
		if (ntree_limit == None):
			ntree_limit = gbm.best_iteration

		pred = gbm.predict(xgb.DMatrix(df_test[features]), ntree_limit=ntree_limit)    	
		return pred

	def cross_validation(self, test_size=0.25, random_state=0):
		part_train, part_test = train_test_split(self.df_train, test_size=test_size, random_state=random_state)
		print ("Partition train size:", len(part_train))
		print ("Partition test size:", len(part_test))
		check = self.run_xgboost(df_train=part_train, df_test=part_test)
		score = log_loss(part_test[self.target], check)
		return score

