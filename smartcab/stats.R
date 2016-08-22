setwd("~/Desktop/smartcab/smartcab")
rm(list=ls())
dir()

#rr <- readLines("random_run.txt")
rr <- readLines("smart_run4.txt")
tail(rr,20)

sar_index <- grep("state-action-reward: ",rr)
sar <- rr[sar_index]
head(sar,20)
remove <- nchar("state-action-reward: ") + 1
sar_r <- NULL
for(i in 1:length(sar)){
    sar_r <- c(sar_r,substr(sar[i],remove,nchar(sar[i])))
}

head(sar_r)
unique(sar_r)
sar_f <- data.frame(matrix(unlist(strsplit(sar_r,",")),ncol=8,byrow=T))
head(sar_f,20)

colnames(sar_f) <- c("s.light","s.left","s.oncoming","s.right","s.next","action","reward","visits")
summary(sar_f)

nrow(unique(sar_f[,-c(7,8)]))

temp <- NULL
for(i in 1:nrow(sar_f)){
    temp2 <- NULL
    for(j in 1:(ncol(sar_f)-2)){
        temp2 <- paste(temp2,sar_f[i,j])
    }
    temp <- c(temp,temp2)
}
length(unique(temp))
table(sar_f$visits)
length(summary(sar_f))
str(sar_f)
nrow(sar_f)

sar_index <- grep("Environment.act",rr)
status <- rr[sar_index]
status

sar_index <- grep("deadline",rr)
deadline <- rr[sar_index]
deadline
remove <- nchar("Environment.reset(): Trial set up with start = (")

time <- NULL
destination <- NULL
start  <- NULL
for(i in 1:length(deadline)){
    start <- c(start,substr(deadline[i],49,49),substr(deadline[i],52,52))
    destination <- c(destination,substr(deadline[i],71,71),substr(deadline[i],74,74))
    time <- c(time,substr(deadline[i],89,90))
}
time
start <- data.frame(matrix(start,ncol=2,byrow = T))
destination <- data.frame(matrix(destination,ncol=2,byrow = T))
time <- data.frame(matrix(time,ncol=1,byrow = T))

colnames(start) <- c("x","y")
colnames(destination) <- c("x","y")
colnames(time) <- c("timestep")

start$x <- as.numeric(as.character(start$x))
start$y <- as.numeric(as.character(start$y))

destination$x <- as.numeric(as.character(destination$x))
destination$y <- as.numeric(as.character(destination$y))

time <- as.numeric(as.character(time$timestep))

summary(time)

distances <- abs(start$x-destination$x) + abs(start$y-destination$y)
summary(distances)


index <- grep("RoutePlanner.route_to",rr)+1
total <- rr[index]
total
total <- as.numeric(as.character(total))
total

plot(total/index,type="l",pch=20)

index2 <- index[2:length(index)]-index[1:(length(index)-1)]
index2 <- c(6,index2)
index2
plot(index2/distances)
plot(total/index,type="l")

