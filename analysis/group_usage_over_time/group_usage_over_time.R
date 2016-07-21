library("data.table")

setwd("~/development/kaggle-talking-data")

##### FUNCTIONS #####
time.to.decimal <- function(time){
  hour = strftime(time, format = "%H")
  min = strftime(time, format = "%M")
  min_decimal = as.integer(min) / 60
  
  time_decimal = as.integer(hour) + min_decimal 
  time_decimal =  round(time_decimal, 2)
  time_decimal
}

fill.with.zeros <- function(tab){
  table.df = data.frame(tab)
  keys = table.df$Var1
  for (i in 0:23){
    if (! is.element(i, keys)){
      table.df = rbind(table.df, data.frame("Var1"=as.character(i), "Freq"=0))
    }
  }
  table.df
}

plot.freq.over.time <- function(column, title){
  title = unique(title)
  freq = table(round(column))
  freq.relative = freq / length(column)

  freq.relative = fill.with.zeros(freq.relative)
  colnames(freq.relative) = c("hour", "freq")
  
  #sorting by hour label
  freq.relative$hour = as.numeric(freq.relative$hour)
  freq.relative$freq = as.numeric(freq.relative$freq)
  freq.relative = freq.relative[with(freq.relative, order(hour)), ]
  print (freq.relative)

  barplot(height = freq.relative$freq, names.arg = freq.relative$hour, col = "lightgreen", main = title, ylim = c(0,1))
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

##### PLOTTING EVENTS BY AGE OVER TIME #####

#remove rows with no age information
evts.gnda = evts.gnda[! is.na(evts.gnda$age),]
#using data.table for the following grouping plot
evts.gnda = data.table(evts.gnda)
setkey(evts.gnda, age)
#grouping plot
plots = evts.gnda[, plot.freq.over.time(time.decimal, age), by = age]


