setwd("~/dev/kaggle-talking-data")

##### FUNCTIONS #####
time.to.decimal <- function(time){
  hour = strftime(time, format = "%H")
  min = strftime(time, format = "%M")
  min_decimal = as.integer(min) / 60
  
  time_decimal = as.integer(hour) + min_decimal 
  time_decimal =  round(time_decimal, 2)
  time_decimal
}

plot.freq.over.time <- function(column, title){
  title = unique(title)
  freq = table(round(column))
  freq.relative = freq / length(column)
  barplot(freq.relative, col = "lightgreen", main = title, ylim = c(0,1))
}

##### LOADING #####
evts.classes = c("integer", "factor", "character", "numeric", "numeric")
evts = read.csv("data/events.csv", colClasses = evts.classes)

gnda.classes = c("factor", "factor", "factor", "factor")
gnda = read.csv("data/gender_age_train.csv", colClasses = gnda.classes)

##### FORMATING DATA #####
evts.gnda = merge(evts, gnda, by = "device_id", all.x = TRUE)
gnda = NULL
evts = NULL
evts.gnda$event_id = NULL
gc()

evts.gnda$time.decimal = time.to.decimal(evts.gnda$timestamp)

evts.gnda$timestamp = NULL
gc()

##### PLOTTING EVENTS BY AGE OVER TIME #####
aggregate(time.decimal ~ age, evts.gnda[! is.na(evts.gnda$age),], plot.freq.over.time)


evts.age.clean = evts.gnda[! is.na(evts.gnda$age),]
evts.age.clean = data.table(evts.age.clean)
setkey(evts.age.clean, age)
#aggregating - recommending
plots = evts.age.clean[, plot.freq.over.time(time.decimal, age), by = age]



