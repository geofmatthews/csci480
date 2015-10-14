set.seed(999)
setwd("I:/csci480/lectures/noise/")

#dev.new(width=8,height=3)
par(mai=c(0.8,0.8,0.1,0.1))

noiseTable <- c(0.0, 0.14, 0.29, 0.43, 0.57, 0.71, 0.86, 1.00)
hashTable <- c(4,7,6,2,0,3,1,5)
latticeNoise <- function(x) {
  return (noiseTable[hashTable[x %% 8]])
}

lerp <- function(pct, a, b) {
  return (a + pct*(b-a))
}
lerpNoise <- function(x) {
  a <- latticeNoise(floor(x))
  b <- latticeNoise(floor(x)+1)
  pct <- x - floor(x)
  return (lerp(pct, a, b))
}

x <- seq(1,10,1)
Noise <- latticeNoise(x)

plot(x,Noise,pch=21,bg="red",xaxp=c(1,20,19),ylim=c(0,1))
dev.copy2eps(file="randompoints.eps")

lines(x,Noise)
dev.copy2eps(file="randomlerped.eps")


smoothlerp <- function(pct, a, b) {
  scale <- b-a
  if (pct < 0.5) {
    return ((2*pct*pct)* scale + a)
  } else {
    pct <- 1.0-pct
    return ((1.0 - 2*pct*pct)* scale + a)
  }
}

smoothnoise <- function(x) {
  intx <- floor(x)
  a <- Noise[intx]
  b <- Noise[intx+1]
  pct <- x - intx
  value <- smoothlerp(pct, a, b)
  return (value)
}

xx <- seq(1,10-0.05,.05)

plot(x,Noise,pch=21,bg="red",xaxp=c(1,20,19),ylim=c(0,1))
lines(xx,sapply(xx,smoothnoise))
dev.copy2eps(file="randomsmoothed.eps")
  




  
