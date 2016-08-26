import pandas as pd
import numpy as np
%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import csr_matrix, hstack
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import log_loss
from scipy.io import mmwrite
import gc
from os import chdir

####################################################### Load Data ####################################################### 

working_dir = "/home/henrique/DataScience/talking_data"
chdir(working_dir)

gatrain = pd.read_csv('data_files/gender_age_train.csv', index_col='device_id')

gatest = pd.read_csv('data_files/gender_age_test.csv', index_col = 'device_id')

phone = pd.read_csv('data_files/phone_brand_device_model.csv')

# Get rid of duplicate device ids in phone
phone = phone.drop_duplicates('device_id',keep='first').set_index('device_id')

events = pd.read_csv('data_files/events.csv', parse_dates=['timestamp'], index_col='event_id')

appevents = pd.read_csv('data_files/app_events.csv', 
                        usecols=['event_id','app_id','is_active'],
                        # nrows=300000,
                        dtype={'is_active':bool})
                        
applabels = pd.read_csv('data_files/app_labels.csv')

####################################################### Phone Brand ####################################################### 

gatrain['trainrow'] = np.arange(gatrain.shape[0])
gatest['testrow'] = np.arange(gatest.shape[0])

phone['brand'] = LabelEncoder().fit_transform(phone.phone_brand)

gatrain['brand'] = phone['brand']
gatest['brand'] = phone['brand']

Xtr_brand = csr_matrix((np.ones(gatrain.shape[0]), 
                       (gatrain.trainrow, gatrain.brand)))
Xte_brand = csr_matrix((np.ones(gatest.shape[0]), 
                       (gatest.testrow, gatest.brand)))
                       
print('Brand features: train shape {}, test shape {}'.format(Xtr_brand.shape, Xte_brand.shape))

####################################################### Phone Model ####################################################### 

brand_model = phone.phone_brand.str.cat(phone.device_model)

phone['model'] = LabelEncoder().fit_transform(brand_model)

gatrain['model'] = phone['model']
gatest['model'] = phone['model']

Xtr_model = csr_matrix((np.ones(gatrain.shape[0]), 
                       (gatrain.trainrow, gatrain.model)))
Xte_model = csr_matrix((np.ones(gatest.shape[0]), 
                       (gatest.testrow, gatest.model)))
                       
print('Model features: train shape {}, test shape {}'.format(Xtr_model.shape, Xte_model.shape))


####################################################### Installed Apps Features ####################################################### 

appencoder = LabelEncoder().fit(appevents.app_id)
appevents['app'] = appencoder.transform(appevents.app_id)
napps = len(appevents['app'].unique())

unique_app_ids = appevents.app_id.unique()

appevents = (appevents.merge(events[['device_id']], how='left',left_on='event_id',right_index=True)
                       .groupby(['device_id','app'])['app'].agg(['size'])
                       .merge(gatrain[['trainrow']], how='left', left_index=True, right_index=True)
                       .merge(gatest[['testrow']], how='left', left_index=True, right_index=True)
                       .reset_index())

appevents.head()

gc.collect()

d = appevents.dropna(subset=['trainrow'])
Xtr_app = csr_matrix((np.ones(d.shape[0]), (d.trainrow, d.app)), 
                      shape=(gatrain.shape[0],napps))
                

d = appevents.dropna(subset=['testrow'])
Xte_app = csr_matrix((np.ones(d.shape[0]), (d.testrow, d.app)), 
                      shape=(gatest.shape[0],napps))

print('Apps data: train shape {}, test shape {}'.format(Xtr_app.shape, Xte_app.shape))


####################################################### App Label Features ####################################################### 

#filter applabels to have only app_ids that are in app_events
applabels = applabels.loc[applabels.app_id.isin(unique_app_ids)]

applabels['app'] = appencoder.transform(applabels.app_id)

applabels['label'] = LabelEncoder().fit_transform(applabels.label_id)
nlabels = len(applabels['label'].unique())

devicelabels = (appevents[['device_id','app']]
                .merge(applabels[['app','label']])
                .groupby(['device_id','label'])['app'].agg(['size'])
                .merge(gatrain[['trainrow']], how='left', left_index=True, right_index=True)
                .merge(gatest[['testrow']], how='left', left_index=True, right_index=True)
                .reset_index())
                
devicelabels.head()

d = devicelabels.dropna(subset=['trainrow'])
Xtr_label = csr_matrix((np.ones(d.shape[0]), (d.trainrow, d.label)), 
                      shape=(gatrain.shape[0],nlabels))
d = devicelabels.dropna(subset=['testrow'])
Xte_label = csr_matrix((np.ones(d.shape[0]), (d.testrow, d.label)), 
                      shape=(gatest.shape[0],nlabels))
print('Labels data: train shape {}, test shape {}'.format(Xtr_label.shape, Xte_label.shape))


####################################################### Top App Period Features ####################################################### 

device_top_intalled_apps = pd.read_csv('data_files_ready/device_top_active_apps_by_period.csv', sep=';')

device_top_intalled_apps =  device_top_intalled_apps.pivot(index='device_id', columns='timestamp', values='app_id')

device_top_intalled_apps = (device_top_intalled_apps.merge(gatrain[['trainrow']], how='left', left_index=True, right_index=True)
                .merge(gatest[['testrow']], how='left', left_index=True, right_index=True)).reset_index()
                

# afternoon

period = 'afternoon'

device_top_intalled = device_top_intalled_apps.dropna(subset=[period])

device_top_intalled[period] = LabelEncoder().fit_transform(device_top_intalled[period])

napps = len(device_top_intalled[period].unique())

d = device_top_intalled.dropna(subset=['trainrow'])
Xtr_top_afternoon = csr_matrix((np.ones(d.shape[0]), (d.trainrow, d.afternoon)), 
                      shape=(gatrain.shape[0],napps))
                      
d = device_top_intalled.dropna(subset=['testrow'])
Xte_top_afternoon = csr_matrix((np.ones(d.shape[0]), (d.testrow, d.afternoon)), 
                      shape=(gatest.shape[0],napps))

# breakfast

period = 'breakfast'

device_top_intalled = device_top_intalled_apps.dropna(subset=[period])

device_top_intalled[period] = LabelEncoder().fit_transform(device_top_intalled[period])

napps = len(device_top_intalled[period].unique())

d = device_top_intalled.dropna(subset=['trainrow'])
Xtr_top_breakfast = csr_matrix((np.ones(d.shape[0]), (d.trainrow, d.breakfast)), 
                      shape=(gatrain.shape[0],napps))
                      
d = device_top_intalled.dropna(subset=['testrow'])
Xte_top_breakfast = csr_matrix((np.ones(d.shape[0]), (d.testrow, d.breakfast)), 
                      shape=(gatest.shape[0],napps))

# dawn

period = 'dawn'

device_top_intalled = device_top_intalled_apps.dropna(subset=[period])

device_top_intalled[period] = LabelEncoder().fit_transform(device_top_intalled[period])

napps = len(device_top_intalled[period].unique())

d = device_top_intalled.dropna(subset=['trainrow'])
Xtr_top_dawn = csr_matrix((np.ones(d.shape[0]), (d.trainrow, d.dawn)), 
                      shape=(gatrain.shape[0],napps))
                      
d = device_top_intalled.dropna(subset=['testrow'])
Xte_top_dawn = csr_matrix((np.ones(d.shape[0]), (d.testrow, d.dawn)), 
                      shape=(gatest.shape[0],napps))

# dinner

period = 'dinner'

device_top_intalled = device_top_intalled_apps.dropna(subset=[period])

device_top_intalled[period] = LabelEncoder().fit_transform(device_top_intalled[period])

napps = len(device_top_intalled[period].unique())

d = device_top_intalled.dropna(subset=['trainrow'])
Xtr_top_dinner = csr_matrix((np.ones(d.shape[0]), (d.trainrow, d.dinner)), 
                      shape=(gatrain.shape[0],napps))
                      
d = device_top_intalled.dropna(subset=['testrow'])
Xte_top_dinner = csr_matrix((np.ones(d.shape[0]), (d.testrow, d.dinner)), 
                      shape=(gatest.shape[0],napps))


# lunch

period = 'lunch'

device_top_intalled = device_top_intalled_apps.dropna(subset=[period])

device_top_intalled[period] = LabelEncoder().fit_transform(device_top_intalled[period])

napps = len(device_top_intalled[period].unique())

d = device_top_intalled.dropna(subset=['trainrow'])
Xtr_top_lunch = csr_matrix((np.ones(d.shape[0]), (d.trainrow, d.lunch)), 
                      shape=(gatrain.shape[0],napps))
                      
d = device_top_intalled.dropna(subset=['testrow'])
Xte_top_lunch = csr_matrix((np.ones(d.shape[0]), (d.testrow, d.lunch)), 
                      shape=(gatest.shape[0],napps))


# morning

period = 'morning'

device_top_intalled = device_top_intalled_apps.dropna(subset=[period])

device_top_intalled[period] = LabelEncoder().fit_transform(device_top_intalled[period])

napps = len(device_top_intalled[period].unique())

d = device_top_intalled.dropna(subset=['trainrow'])
Xtr_top_morning = csr_matrix((np.ones(d.shape[0]), (d.trainrow, d.morning)), 
                      shape=(gatrain.shape[0],napps))
                      
d = device_top_intalled.dropna(subset=['testrow'])
Xte_top_morning = csr_matrix((np.ones(d.shape[0]), (d.testrow, d.morning)), 
                      shape=(gatest.shape[0],napps))


# night

period = 'night'

device_top_intalled = device_top_intalled_apps.dropna(subset=[period])

device_top_intalled[period] = LabelEncoder().fit_transform(device_top_intalled[period])

napps = len(device_top_intalled[period].unique())

d = device_top_intalled.dropna(subset=['trainrow'])
Xtr_top_night = csr_matrix((np.ones(d.shape[0]), (d.trainrow, d.night)), 
                      shape=(gatrain.shape[0],napps))
                      
d = device_top_intalled.dropna(subset=['testrow'])
Xte_top_night = csr_matrix((np.ones(d.shape[0]), (d.testrow, d.night)), 
                      shape=(gatest.shape[0],napps))


####################################################### Concatenate All Features ####################################################### 

Xtrain = hstack((Xtr_brand, Xtr_model, Xtr_app, Xtr_label, Xtr_top_afternoon, Xtr_top_breakfast, Xtr_top_dawn, Xtr_top_dinner, Xtr_top_lunch, Xtr_top_morning, Xtr_top_night), format='csr')
Xtest =  hstack((Xte_brand, Xte_model, Xte_app, Xte_label,  Xte_top_afternoon, Xte_top_breakfast, Xte_top_dawn, Xte_top_dinner, Xte_top_lunch, Xte_top_morning, Xte_top_night), format='csr')
print('All features: train shape {}, test shape {}'.format(Xtrain.shape, Xtest.shape))

####################################################### Cross Validation ####################################################### 

targetencoder = LabelEncoder().fit(gatrain.group)
y = targetencoder.transform(gatrain.group)
nclasses = len(targetencoder.classes_)

def score(clf, random_state = 0):
    kf = StratifiedKFold(y, n_folds=5, shuffle=True, random_state=random_state)
    pred = np.zeros((y.shape[0],nclasses))
    for itrain, itest in kf:
        Xtr, Xte = Xtrain[itrain, :], Xtrain[itest, :]
        ytr, yte = y[itrain], y[itest]
        clf.fit(Xtr, ytr)
        pred[itest,:] = clf.predict_proba(Xte)
        # Downsize to one fold only for kernels
        return log_loss(yte, pred[itest, :])
        print("{:.5f}".format(log_loss(yte, pred[itest,:])), ' ')
    print('')
    return log_loss(y, pred)


Cs = np.logspace(-3,0,4)
res = []
for C in Cs:
    res.append(score(LogisticRegression(C = C)))
plt.semilogx(Cs, res,'-o');

score(LogisticRegression(C=0.03))

score(LogisticRegression(C=0.02, multi_class='multinomial',solver='lbfgs'))

####################################################### Predict on test Data ####################################################### 

clf = LogisticRegression(C=0.02, multi_class='multinomial',solver='lbfgs')
clf.fit(Xtrain, y)
pred = pd.DataFrame(clf.predict_proba(Xtest), index = gatest.index, columns=targetencoder.classes_)
pred.head()

working_dir = "/home/henrique/DataScience/talking_data"
chdir(working_dir)

pred.to_csv('logreg_subm_2.27332.csv',index=True)

# gatest = gatrain = appevents = d = events = applabels = devicelabels = m = phone = None

# Xte_app = Xte_brand = Xte_label = Xte_model = Xtr_app = Xtr_brand = Xtr_label = Xtr_model = None

# gc.collect()

# Xtrain.toarray()[2]

# mmwrite("file.mtx", Xtrain)


                      
