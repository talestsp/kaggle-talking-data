
params = {}
params['bst:max_depth'] = 5 #depth of decision tree, the higher it is increases the overfitting
params['bst:eta'] = 0.2 = #makes the model more robust by shrinking the weights on each step
params['silent'] = 0 #feedback running prints
params['objective'] = "multi:softprob" #output a vector of ndata * nclass
params['nthread'] = 2 #number of parallel threads used to run xgboost
params['eval_metric'] = 'mlogloss' #multiclass logloss 
params['subsample'] = 0.65 #portion of data instances that XGBoost randomly collects to grow trees to prevent overfitting
params['colsample_bytree'] = 0.8 #subsample ratio of columns when constructing each tree
params['n_class'] = 12

num_boost_round = 500 #number of boosting iterations.
early_stopping_rounds = 50 #??


