library(data.table)

setwd("/home/tales/development/kaggle-talking-data/")

gender.train = fread("data/gender_age_train.csv", colClasses = c("character","character","numeric","character"))
gender.test = fread("data/gender_age_test.csv", colClasses = c("character"))
events = fread("data/events.csv", colClasses = c("character","character","character", "numeric","numeric"))

nrow(events)

#events with training devices
nrow(events[is.element(events$device_id, gender.train$device_id),])

#events with testing devices
nrow(events[is.element(events$device_id, gender.test$device_id),])

#events with both
nrow(events[is.element(events$device_id, gender.train$device_id) | is.element(events$device_id, gender.test$device_id),])


nrow(gender.train)
c = is.element(gender.train$device_id, events$device_id)
gender.train2 = gender.train[c,]
nrow(gender.train2)

