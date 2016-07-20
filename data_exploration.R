options(scipen = 999)

setwd("~/development/kaggle-talking-data/")

app.labels = read.csv("data/app_labels.csv")
label.categ = read.csv("data/label_categories.csv")

# app.labels
app.categ = merge(x = app.labels, y = label.categ, by = "label_id")
app.categ$label_id = NULL

#analyzing repeated rows
rep.app.labels.freq = table(paste(paste(app.labels$app_id, app.labels$label_id)))
rep.app.labels.freq = data.frame(sort(rep.app.labels.freq, decreasing = T))
head(rep.app.labels.freq)

