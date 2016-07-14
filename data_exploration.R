options(scipen = 999)

app.labels = read.csv("~/development/talking-data/data/app_labels.csv")
label.categ = read.csv("~/development/talking-data/data/label_categories.csv")
app.events = read.csv("~/development/talking-data/data/app_events.csv")

events = read.csv("~/development/talking-data/data/events.csv")

# app.labels
app.categ = merge(x = app.labels, y = label.categ, by = "label_id")
app.labels.freq = data.frame(sort(table(app.categ$category), decreasing = T))
