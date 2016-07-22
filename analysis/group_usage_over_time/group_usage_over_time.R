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

#removing age == NA
evts.gnda = evts.gnda[! is.na(evts.gnda$age),]

for (i in sort(unique(evts.gnda$age))){
  #barplot(table(evts.gnda$time.decimal), names.arg = i)
  print (i)
  data = evts.gnda[evts.gnda$age == i,]
  round.time = round( data$time.decimal )
  tab = sort(table(round.time), decreasing = T)
  print (tab)
  print ("---")
  print ("")
}




