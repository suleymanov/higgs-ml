# Higgs-ML summary
Rail Suleymanov  
Monday, February 02, 2015  

# Load data
## Training data
Read training data, find number of missing points for each variable, remove missing points.

```r
train_f <- "training.csv"
train <- read.csv(train_f)
train_no_na <- data.frame(train)
features <- colnames(train)
nas1 <- vector("integer", length = length(features))
for (feature in seq_along(features)) {
    ina <- train[, feature] == -999.0
    nas1[feature] <- sum(ina)
}
for (feature in seq_along(features)) {
    ina <- train_no_na[, feature] == -999.0
    train_no_na <- train_no_na[!ina, ]
}
```

Number of missing values for each variable.

```r
library(ggplot2)
```

```
## Warning: package 'ggplot2' was built under R version 3.1.2
```

```r
nas <- data.frame(features, nas1)
nas <- nas[nas1 != 0, ]
q <- qplot(x = features, y = nas1, data = nas, geom = "bar", stat = "identity")
q + theme(axis.text.x = element_text(angle = 90)) + xlab("Number of missing values")
```

![](higgs_summary_files/figure-html/unnamed-chunk-2-1.png) 

Check if there are full matching na's in different features. That can be the case in variables **DER_deltaeta_jet_jet** (6-th variable), **DER_mass_jet_jet** (7-th), **DER_prodeta_jet_jet** (8-th), **DER_lep_eta_centrality** (14-th), **PRI_jet_subleading_pt** (28-th), **PRI_jet_subleading_eta** (29-th), **PRI_jet_subleading_phi** (30-th) and in variables **PRI_jet_leading_pt** (25-th), **PRI_jet_leading_eta** (26-th), **PRI_jet_leading_phi** (27-th).

```r
ina6 <- which(train$DER_deltaeta_jet_jet == -999)
ina7 <- which(train$DER_mass_jet_jet == -999)
ina8 <- which(train$DER_prodeta_jet_jet == -999)
ina14 <- which(train$DER_lep_eta_centrality == -999)
ina28 <- which(train$PRI_jet_subleading_pt == -999)
ina29 <- which(train$PRI_jet_subleading_eta == -999)
ina30 <- which(train$PRI_jet_subleading_phi == -999)

match_res <- sum(intersect(ina6, ina7) == ina6) == length(ina7)
match_res <- sum(intersect(ina6, ina8) == ina6) == length(ina8)
match_res <- sum(intersect(ina6, ina14) == ina6) == length(ina14)
match_res <- sum(intersect(ina6, ina28) == ina6) == length(ina28)
match_res <- sum(intersect(ina6, ina29) == ina6) == length(ina29)
match_res <- sum(intersect(ina6, ina30) == ina6) == length(ina30)
```

Do all na's in those variables match? TRUE


```r
ina25 <- which(train$PRI_jet_leading_pt == -999.0)
ina26 <- which(train$PRI_jet_leading_eta == -999.0)
ina27 <- which(train$PRI_jet_leading_phi == -999.0)

match_res <- sum(intersect(ina25, ina26) == ina25) == length(ina26)
match_res <- sum(intersect(ina25, ina27) == ina27) == length(ina27)
```

Do all na's in those variables match? TRUE

We see that there's indeed full matching of these features. Now let's explore how do indexes of NA features intersect for **DER_mass_MMC**, **DER_deltaeta_jet_jet** and **PRI_jet_leading_pt**.

```r
library(VennDiagram)
```

```
## Warning: package 'VennDiagram' was built under R version 3.1.2
```

```
## Loading required package: grid
```

```r
ina2 <- which(train$DER_mass_MMC == -999)
area1 <- length(ina6)
area2 <- length(ina2)
area3 <- length(ina25)
in12 <- length(intersect(ina6, ina2))
in13 <- length(intersect(ina6, ina25))
in23 <- length(intersect(ina2, ina25))
in123 <- length(intersect(ina6, intersect(ina2, ina25)))

venn.plot <- draw.triple.venn(area1, area2, area3, in12, in23, in13, in123, 
                              category = c("DER_deltaeta_jet_jet", "DER_mass_jet_jet", "PRI_jet_leading_pt"),
                              fill = c("blue", "red", "green"),
                              lty = "blank", cat.col = rep("black", 3))
```

![](higgs_summary_files/figure-html/unnamed-chunk-5-1.png) 


## Test data
Read test data, find number of missing points for each variable, remove missing points.

```r
test_f <- "test.csv"
test <- read.csv(test_f)
test_no_na <- data.frame(test)
features <- colnames(test)
nas2 <- vector("integer", length = length(features))
for (feature in seq_along(features)) {
    ina <- test[, feature] == -999.0
    nas2[feature] <- sum(ina)
}
for (feature in seq_along(features)) {
    ina <- test_no_na[, feature] == -999.0
    test_no_na <- test_no_na[!ina, ]
}
```

Number of missing values for each variable.

```r
nas <- data.frame(features, nas2)
nas <- nas[nas2 != 0, ]
q <- qplot(x = features, y = nas2, data = nas, geom = "bar", stat = "identity")
q + theme(axis.text.x = element_text(angle = 90)) + xlab("Number of missing values")
```

![](higgs_summary_files/figure-html/unnamed-chunk-7-1.png) 

Perform same na's matching for test set as it was for training set

```r
ina6 <- which(test$DER_deltaeta_jet_jet == -999)
ina7 <- which(test$DER_mass_jet_jet == -999)
ina8 <- which(test$DER_prodeta_jet_jet == -999)
ina14 <- which(test$DER_lep_eta_centrality == -999)
ina28 <- which(test$PRI_jet_subleading_pt == -999)
ina29 <- which(test$PRI_jet_subleading_eta == -999)
ina30 <- which(test$PRI_jet_subleading_phi == -999)

match_res <- sum(intersect(ina6, ina7) == ina6) == length(ina7)
match_res <- sum(intersect(ina6, ina8) == ina6) == length(ina8)
match_res <- sum(intersect(ina6, ina14) == ina6) == length(ina14)
match_res <- sum(intersect(ina6, ina28) == ina6) == length(ina28)
match_res <- sum(intersect(ina6, ina29) == ina6) == length(ina29)
match_res <- sum(intersect(ina6, ina30) == ina6) == length(ina30)
```

Do all na's in those variables match? TRUE


```r
ina25 <- which(test$PRI_jet_leading_pt == -999.0)
ina26 <- which(test$PRI_jet_leading_eta == -999.0)
ina27 <- which(test$PRI_jet_leading_phi == -999.0)

match_res <- sum(intersect(ina25, ina26) == ina25) == length(ina26)
match_res <- sum(intersect(ina25, ina27) == ina27) == length(ina27)
```

Do all na's in those variables match? TRUE

We see that there's indeed full matching of these features. Now let's explore how do indexes of NA features intersect for **DER_mass_MMC**, **DER_deltaeta_jet_jet** and **PRI_jet_leading_pt**.

```r
library(VennDiagram)
ina2 <- which(test$DER_mass_MMC == -999)
area1 <- length(ina6)
area2 <- length(ina2)
area3 <- length(ina25)
in12 <- length(intersect(ina6, ina2))
in13 <- length(intersect(ina6, ina25))
in23 <- length(intersect(ina2, ina25))
in123 <- length(intersect(ina6, intersect(ina2, ina25)))

venn.plot <- draw.triple.venn(area1, area2, area3, in12, in23, in13, in123, 
                              category = c("DER_deltaeta_jet_jet", "DER_mass_MMC", "PRI_jet_leading_pt"),
                              fill = c("blue", "red", "green"),
                              lty = "blank", cat.col = rep("black", 3))
```

![](higgs_summary_files/figure-html/unnamed-chunk-10-1.png) 

# Conclusion
According to NA's structure investigation, 2 strategies are possible:
1. As there's complete NA-matching between several sets of variables, we can conclude that whole dataset can be divided to following parts
 - examples having all variables defined (i.e. without indexes that go into coloured regions on the last figure) - set A
 - examples that didn't go to 'set A', having all variables defined except variable **DER_mass_MMC** (coloured red) - set B
 - examples that didn't go to previous sets, having all variables defined except variable **DER_deltaeta_jet_jet** (coloured blue) - set C
 - examples that didn't go to previous sets, having all variables defined except variables **DER_mass_MMC** AND **DER_deltaeta_jet_jet** (coloured purple) - set D
 - examples that didn't go to previous sets, having all variables defined except variables **DER_deltaeta_jet_jet** AND **PRI_jet_leading_pt** (light green) - set E
 - examples that didn't go to previous sets, having all variables defined except variables **DER_mass_MMC**, **DER_deltaeta_jet_jet** AND **PRI_jet_leading_pt** (dark green, the intersection of all 3 regions) - set F
2. Leave dataset 'asis' but then need to fill NA's using algorithm one of
 - variable means
 - generate randoms from that variable's distributions
 - k-nearest neighbors
 - k-means clustering

# Details of some of features

```r
s_train <- summary(train_no_na)
s_test <- summary(test_no_na)
```

## 1) Estimated mass of the Higgs boson candidate (DER_mass_MMC)

```r
main <- "Histogram of DER_mass_MMC"
xlab <- "DER_mass_MMC"
ylab <- "Frequency"
leg <- c("Test", "Train")
hist(test_no_na$DER_mass_MMC, 
     breaks = 50, col = "red", xlab = xlab, ylab = ylab, main = main, xlim = c(0, 500))
hist(train_no_na$DER_mass_MMC, breaks = 50, col = "blue", add = T)
legend("topright", pch = 1, col = c("red", "blue"), legend = leg)
```

![](higgs_summary_files/figure-html/unnamed-chunk-12-1.png) 

Test set statistics: Min.   :   9.112  , 1st Qu.:  93.348  , Median : 113.455  , Mean   : 122.771  , 3rd Qu.: 133.674  , Max.   :1949.261  

Train set statistics: Min.   :  9.878  , 1st Qu.: 93.320  , Median :113.230  , Mean   :122.816  , 3rd Qu.:133.456  , Max.   :988.199  

## 2) Transverse mass between the missing transverse energy and the lepton (DER_mass_transverse_met_lep)

```r
main <- "Histogram of DER_mass_transverse_met_lep"
xlab <- "DER_mass_transverse_met_lep"
ylab <- "Frequency"
leg <- c("Test", "Train")
hist(test_no_na$DER_mass_transverse_met_lep, 
     breaks = 50, col = "red", xlab = xlab, ylab = ylab, main = main, xlim = c(0, 200))
hist(train_no_na$DER_mass_transverse_met_lep, breaks = 50, col = "blue", add = T)
legend("topright", pch = 1, col = c("red", "blue"), legend = leg)
```

![](higgs_summary_files/figure-html/unnamed-chunk-13-1.png) 

Test set statistics: Min.   :  0.00  , 1st Qu.: 11.42  , Median : 26.93  , Mean   : 35.10  , 3rd Qu.: 51.63  , Max.   :527.92  

Train set statistics: Min.   :  0.00  , 1st Qu.: 11.32  , Median : 26.96  , Mean   : 35.27  , 3rd Qu.: 52.20  , Max.   :594.29  

## 3) Invariant mass of the hadronic tau and the lepton (DER_mass_vis)

```r
main <- "Histogram of DER_mass_vis"
xlab <- "DER_mass_vis"
ylab <- "Frequency"
leg <- c("Test", "Train")
hist(test_no_na$DER_mass_vis, 
     breaks = 50, col = "red", xlab = xlab, ylab = ylab, main = main, xlim = c(0, 200))
hist(train_no_na$DER_mass_vis, breaks = 50, col = "blue", add = T)
legend("topright", pch = 1, col = c("red", "blue"), legend = leg)
```

![](higgs_summary_files/figure-html/unnamed-chunk-14-1.png) 

Test set statistics: Min.   :  7.352  , 1st Qu.: 57.343  , Median : 70.981  , Mean   : 78.623  , 3rd Qu.: 88.442  , Max.   :983.204  

Train set statistics: Min.   :  7.33  , 1st Qu.: 57.27  , Median : 70.93  , Mean   : 78.50  , 3rd Qu.: 88.37  , Max.   :789.54  

## 4) Modulus of the vector sum of the transverse momentum of the hadronic tau, the lepton,
## and the missing transverse energy vector (DER_pt_h)

```r
main <- "Histogram of DER_pt_h"
xlab <- "DER_pt_h"
ylab <- "Frequency"
leg <- c("Test", "Train")
hist(test_no_na$DER_pt_h, 
     breaks = 50, col = "red", xlab = xlab, ylab = ylab, main = main, xlim = c(0, 500))
hist(train_no_na$DER_pt_h, breaks = 50, col = "blue", add = T)
legend("topright", pch = 1, col = c("red", "blue"), legend = leg)
```

![](higgs_summary_files/figure-html/unnamed-chunk-15-1.png) 

Test set statistics: Min.   :   0.112  , 1st Qu.:  57.477  , Median :  94.221  , Mean   : 110.919  , 3rd Qu.: 145.197  , Max.   :1337.187  

Train set statistics: Min.   :   0.12  , 1st Qu.:  57.83  , Median :  94.71  , Mean   : 111.43  , 3rd Qu.: 145.82  , Max.   :1053.81  

## 5) Absolute value of the pseudorapidity separation between the two jets (DER_deltaeta_jet_jet)

```r
main <- "Histogram of DER_deltaeta_jet_jet"
xlab <- "DER_deltaeta_jet_jet"
ylab <- "Frequency"
leg <- c("Test", "Train")
hist(test_no_na$DER_deltaeta_jet_jet, 
     breaks = 50, col = "red", xlab = xlab, ylab = ylab, main = main, xlim = c(0, 10))
hist(train_no_na$DER_deltaeta_jet_jet, breaks = 50, col = "blue", add = T)
legend("topright", pch = 1, col = c("red", "blue"), legend = leg)
```

![](higgs_summary_files/figure-html/unnamed-chunk-16-1.png) 

Test set statistics: Min.   :0.000  , 1st Qu.:0.904  , Median :2.143  , Mean   :2.436  , 3rd Qu.:3.745  , Max.   :8.724  

Train set statistics: Min.   :0.000  , 1st Qu.:0.897  , Median :2.147  , Mean   :2.434  , 3rd Qu.:3.741  , Max.   :8.503  
