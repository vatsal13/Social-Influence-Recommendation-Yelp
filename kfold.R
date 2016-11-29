data  <- read.csv("split_userCustom.csv")
nrFolds <- 10

# generate array containing fold-number for each sample (row)
folds <- rep_len(1:nrFolds, nrow(data))
folds <- sample(folds, nrow(data))
# actual cross validation
for(k in 1:nrFolds) {
  # actual split of the data
  print(k) 
  fold <- which(folds == k)
  #folds <- sample(folds, nrow(data))
  data.train <- data[-fold,]
  data.test <- data[fold,]
  f = paste("test", k, ".csv",sep ="")
  print(f)
  f1 =  paste("train", k, ".csv",sep ="")
  write.csv(data.train, file = f1) 
  write.csv(data.test, file = f)
  # train and test your model with data.train and data.test
}

#data.train
#data.test


