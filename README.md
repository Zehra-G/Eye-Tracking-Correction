# Eye-Tracking-Correction

## What is this project about?

Software traceability using eye trackers has been used since the 1990s. The objective of this study is to review the most common algorithmic solutions for error correction, generally designed to work with natural language reading data, on source code data. Eye tracking data correction algorithms were implemented from Carr et al. (2022), Sanches et al. (2015), Cohen (2013), Lohmeier (2015), Hornof et al. (2011), along with composite algorithms that use the output of multiple different high-performing algorithms.We implemented these algorithms and tested them on real and synthetic data eye tracking data on code reading. As expected, algorithms specific for natural  language did not perform well. With the best performing algorithm being attach with an accuracy of ~20% for real data and ~80% for synthetic data at the word level. Therefore, this study further establishes that algorithms for correcting source code data should be further explored due to its more difficult model. 

<p align="center">
  <img width="327" alt="Screen Shot 2023-05-04 at 14 17 34" src="https://user-images.githubusercontent.com/113384943/236293409-f337efbf-fd2f-40e1-a0ac-f8e9907e7aa0.png">
</p>
Example of Eye Tracking Data On Code. Left: Without Correction, Right: With Correction


## Purpose of The Code & Study

Investigateing and quantifying the accuracy of most correction algorithms on source code.

### Research Questions

* RQ1: Can the same model for natural language be applied to source code?
* RQ2: What are some of the typical errors observed in source code?
* RQ3: Are algorithms specific for natural language applicable to source code?
* RQ4: How do we generate data that resembles source code patterns?
* RQ5: How does each algorithm perform under real and synthetic data? 


## Data

### Real Eye Tracking Data on Code
We used data from Bednarik et al. (2020) which included trials in Java and Python.


![data ](https://user-images.githubusercontent.com/113384943/236294497-4cd49c90-4dee-4860-b8dd-7065b75bd0dc.png)

### Synthetic Eye Tracking Data on Code

* Non-linear (generated using a probability distribution)
* Skipping (based on aoi length and probability distribution) 
* Regression and progression (based on probability parameter)
* Error ( similar to Carr et al. (2022))
* Offset (deviation from aoi by some x,y for all)
* Slope 
* Shift 
* Noise (deviation from aoi by some x,y)

## Results

### Results on Synthetic Data

<p align="center">
<img width="747" alt="Screen Shot 2023-05-04 at 14 32 30" src="https://user-images.githubusercontent.com/113384943/236296783-91a9cebf-2016-4b0c-9ab1-f52d574c9104.png">
</p>

<p align="center">
<img width="750" alt="Screen Shot 2023-05-04 at 14 32 50" src="https://user-images.githubusercontent.com/113384943/236296857-3c198edc-b44a-48fb-8a62-2f777de8fd85.png">
</p>

### Results on Real Data

<p align="center">
<img width="430" alt="Screen Shot 2023-05-04 at 14 33 05" src="https://user-images.githubusercontent.com/113384943/236296913-928bd5a7-aa1c-42ee-98b6-5168fbfdf367.png">
</p>

## Sources 
* Busjahn, T., Bednarik, R., Begel, A., Crosby, M., Paterson, J. H., Schulte, C., ... & Tamm, S. (2015, May). Eye movements in code reading: Relaxing the linear order. In 2015 IEEE 23rd International Conference on Program Comprehension (pp. 255-265). IEEE.

* Carr, J. W., Pescuma, V. N., Furlan, M., Ktori, M., & Crepaldi, D. (2022). Algorithms for the automated correction of vertical drift in eye-tracking data. Behavior Research Methods, 54(1), 287-310.

* Sharafi, Z., Sharif, B., Guéhéneuc, Y. G., Begel, A., Bednarik, R., & Crosby, M. (2020). A practical guide on conducting eye tracking studies in software engineering. Empirical Software Engineering, 25, 3128-3174.

* Hornof, A. J., & Halverson, T. (2002). Cleaning up systematic error in eye-tracking data by using required fixation locations. Behavior Research Methods, Instruments, & Computers, 34(4), 592-604.

* Cohen, A. L. (2013). Software for the automatic correction of recorded eye fixation locations in reading experiments. Behavior research methods, 45, 679-683.

* Sanches, C. L., Kise, K., & Augereau, O. (2015). Eye gaze and text line matching for
reading analysis. Adjunct Proceedings of the 2015 ACM International Joint
Conference on Pervasive and Ubiquitous Computing and Proceedings of the 2015
ACM International Symposium on Wearable Computers, 1227–1233.

* Lohmeier, S. (2015). Experimental evaluation and modelling of the comprehension of
indirect anaphors in a programming language [ma thesis]. Information and Software
Technology.

* Zhang, Y., & Hornof, A. J. (2011). Mode-of-disparities error correction of eye-tracking
data. Behavior research methods, 43, 834–842. 
