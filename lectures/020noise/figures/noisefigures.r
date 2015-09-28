

x <- seq(0,10,.01);
plot(x,sin(x),type="l");
for (freq in seq(2,4)) {
  lines(x,sin(freq*x))
};

white <- function(x) {
  accum <- 0.0
  denom <- 0.0
  for (freq in seq(1,20)) {
     denom <- denom + 1
     accum <- accum + sin(freq*(x+6*runif(1)))
  }
  return (accum/denom)
}

plot(x,white(x),type="l")


pink <- function(x) {
  accum <- 0.0
  denom <- 0.0
  for (freq in seq(1,20)) {
    denom <- denom + 1
    accum <- accum + sin(freq*(x+6*runif(1)))/freq
  }
  return (accum/denom)
}

plot(x,pink(x),type="l")


x <- seq(0,10,.01);
plot(x,sin(x),type="l");
for (freq in seq(2,4)) {
  lines(x,sin(freq*x)/freq)
};

