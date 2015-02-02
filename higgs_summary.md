# Higgs-ML summary
Rail Suleymanov  
Monday, February 02, 2015  

# Load training data
Read training data, find number of missing points for each variable, remove missing points.

```r
train_f <- "training.csv"
train <- read.csv(train_f)
train_no_na <- data.frame(train)
features <- colnames(train)
n_ina <- vector("integer", length = length(features))
for (feature in seq_along(features)) {
    ina <- train[, feature] == -999.0
    n_ina[feature] <- sum(ina)
}
for (feature in seq_along(features)) {
    ina <- train_no_na[, feature] == -999.0
    train_no_na <- train_no_na[!ina, ]
}
```

# Print simple summary on pure variables

```r
summary(train_no_na)
```

```
##     EventId        DER_mass_MMC     DER_mass_transverse_met_lep
##  Min.   :100000   Min.   :  9.878   Min.   :  0.00             
##  1st Qu.:162350   1st Qu.: 93.320   1st Qu.: 11.32             
##  Median :225288   Median :113.230   Median : 26.96             
##  Mean   :225035   Mean   :122.816   Mean   : 35.27             
##  3rd Qu.:287773   3rd Qu.:133.456   3rd Qu.: 52.20             
##  Max.   :349994   Max.   :988.199   Max.   :594.29             
##   DER_mass_vis       DER_pt_h       DER_deltaeta_jet_jet DER_mass_jet_jet
##  Min.   :  7.33   Min.   :   0.12   Min.   :0.000        Min.   :  13.6  
##  1st Qu.: 57.27   1st Qu.:  57.83   1st Qu.:0.897        1st Qu.: 113.5  
##  Median : 70.93   Median :  94.71   Median :2.147        Median : 232.4  
##  Mean   : 78.50   Mean   : 111.43   Mean   :2.434        Mean   : 378.2  
##  3rd Qu.: 88.37   3rd Qu.: 145.82   3rd Qu.:3.741        3rd Qu.: 489.4  
##  Max.   :789.54   Max.   :1053.81   Max.   :8.503        Max.   :4975.0  
##  DER_prodeta_jet_jet DER_deltar_tau_lep   DER_pt_tot        DER_sum_pt    
##  Min.   :-18.066     Min.   :0.228      Min.   :  0.004   Min.   : 110.6  
##  1st Qu.: -2.729     1st Qu.:1.397      1st Qu.:  4.218   1st Qu.: 192.8  
##  Median : -0.284     Median :1.940      Median : 22.542   Median : 246.7  
##  Mean   : -0.881     Mean   :1.997      Mean   : 27.357   Mean   : 281.5  
##  3rd Qu.:  0.921     3rd Qu.:2.574      3rd Qu.: 39.068   3rd Qu.: 331.1  
##  Max.   : 16.648     Max.   :5.579      Max.   :466.525   Max.   :1852.5  
##  DER_pt_ratio_lep_tau DER_met_phi_centrality DER_lep_eta_centrality
##  Min.   : 0.0470      Min.   :-1.4140        Min.   :0.0000        
##  1st Qu.: 0.7622      1st Qu.: 0.1910        1st Qu.:0.0050        
##  Median : 1.2060      Median : 1.0710        Median :0.4690        
##  Mean   : 1.4809      Mean   : 0.6373        Mean   :0.4638        
##  3rd Qu.: 1.8540      3rd Qu.: 1.3420        3rd Qu.:0.8830        
##  Max.   :19.7730      Max.   : 1.4140        Max.   :1.0000        
##    PRI_tau_pt      PRI_tau_eta         PRI_tau_phi          PRI_lep_pt    
##  Min.   : 20.00   Min.   :-2.496000   Min.   :-3.141000   Min.   : 26.00  
##  1st Qu.: 26.59   1st Qu.:-0.889000   1st Qu.:-1.570000   1st Qu.: 33.28  
##  Median : 36.59   Median :-0.011000   Median :-0.010000   Median : 43.45  
##  Mean   : 45.72   Mean   :-0.003367   Mean   : 0.001104   Mean   : 52.43  
##  3rd Qu.: 54.19   3rd Qu.: 0.879750   3rd Qu.: 1.580000   3rd Qu.: 61.48  
##  Max.   :622.86   Max.   : 2.497000   Max.   : 3.142000   Max.   :461.90  
##   PRI_lep_eta         PRI_lep_phi         PRI_met      
##  Min.   :-2.487000   Min.   :-3.1420   Min.   :  0.20  
##  1st Qu.:-0.908750   1st Qu.:-1.5180   1st Qu.: 27.08  
##  Median :-0.009000   Median : 0.0770   Median : 44.29  
##  Mean   :-0.003671   Mean   : 0.0419   Mean   : 54.96  
##  3rd Qu.: 0.904000   3rd Qu.: 1.6090   3rd Qu.: 69.42  
##  Max.   : 2.499000   Max.   : 3.1410   Max.   :951.36  
##   PRI_met_phi        PRI_met_sumet      PRI_jet_num    PRI_jet_leading_pt
##  Min.   :-3.142000   Min.   :  34.32   Min.   :2.000   Min.   :  30.20   
##  1st Qu.:-1.550000   1st Qu.: 239.17   1st Qu.:2.000   1st Qu.:  60.84   
##  Median : 0.005000   Median : 305.17   Median :2.000   Median :  87.37   
##  Mean   : 0.006987   Mean   : 334.68   Mean   :2.304   Mean   : 106.88   
##  3rd Qu.: 1.573000   3rd Qu.: 396.38   3rd Qu.:3.000   3rd Qu.: 131.07   
##  Max.   : 3.142000   Max.   :2003.98   Max.   :3.000   Max.   :1120.57   
##  PRI_jet_leading_eta PRI_jet_leading_phi PRI_jet_subleading_pt
##  Min.   :-4.497000   Min.   :-3.14200    Min.   : 30.00       
##  1st Qu.:-1.339000   1st Qu.:-1.57400    1st Qu.: 37.39       
##  Median : 0.000000   Median :-0.03200    Median : 48.11       
##  Mean   :-0.005791   Mean   :-0.01156    Mean   : 57.92       
##  3rd Qu.: 1.330000   3rd Qu.: 1.55800    3rd Qu.: 66.95       
##  Max.   : 4.499000   Max.   : 3.14100    Max.   :721.46       
##  PRI_jet_subleading_eta PRI_jet_subleading_phi PRI_jet_all_pt   
##  Min.   :-4.50000       Min.   :-3.142000      Min.   :  60.22  
##  1st Qu.:-1.62875       1st Qu.:-1.579000      1st Qu.: 109.47  
##  Median :-0.01400       Median :-0.008000      Median : 154.14  
##  Mean   :-0.01293       Mean   :-0.004782      Mean   : 183.37  
##  3rd Qu.: 1.60400       3rd Qu.: 1.573000      3rd Qu.: 223.60  
##  Max.   : 4.50000       Max.   : 3.142000      Max.   :1633.43  
##      Weight         Label    
##  Min.   :0.001502   b:36220  
##  1st Qu.:0.001503   s:31894  
##  Median :0.064061            
##  Mean   :0.445788            
##  3rd Qu.:0.744056            
##  Max.   :7.805035
```
