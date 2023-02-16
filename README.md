# DroidCtxBin_Detection
## Introduction
This is the implementation of BinCtx. Our works aims at identifying undesired/malicious behaviors in Android apps. BinCtx contains two phases: (1) training phase, and (2) prediction phase.

During the training phase, BinCtx first extracts three types of features: (1) the bytecode of an app to model the app's behaviors as a whole instead of focusing on the sensitive API calls as many undesired behaviors are not related to sensitive API calls, (2) the contextual information from metadata file as the whole app's configuration and GUI layouts can introduce a large number of noise, and (2) the usage patterns of third-party library because many apps can abuse those library to achieve certain undesired behaviors. Next, we convert the bytecode into 3-channel RGB images and harness the power of image classification techniques to embedding the bytecode representations. For the contextual features and usage patterns, we use the one-hot representations as they do not contain sequancial or spatial relationships among those features.

During the prediction phase, given an app's bytecode representation, contextual features, URLs, and usage patterns of third-party libraries, BinCtx identifies the corresponding undesired/malicious behaviors via learned model.

![image](https://github.com/DroidCtxBin/BinCtx_Detection/blob/main/overview.jpg)

To evaluate the effectiveness of BinCtx, we collect several malware families from AMD dataset[1]. As the existing malware dataset can be out-of-date, we also resort to the labeled dataset from CHAMP[2], which contains 2,992 recent, real-world apps from Google Play and top-tier Chinese app markets. We merge two datasets as certain undesired behaviors share common characteristics with malware.

## Contents


## Requirements
* Java version: 1.8.0_181
* Python version: 3.7.2
* Tensorflow version: 1.15.0
* ther dependencies: numpy, scikit-learn, pandas
* APKTool: Check https://ibotpeaches.github.io/Apktool/ for more details and download.


[1] Fengguo Wei, Yuping Li, Sankardas Roy, Xinming Ou, and Wu Zhou. Deep ground truth analysis of current android malware. In Michalis Polychronakis and Michael Meier, editors, Proceedings of the International Conference on Detection of Intrusions and Malware, and Vulnerability Assessment (DIMVA), 2017.

[2] Yangyu Hu, Haoyu Wang, Tiantong Ji, Xusheng Xiao, Xiapu Luo, Peng Gao, and Yao Guo. CHAMP: Characterizing undesired app behaviors from user comments based on market policies. In Proceedings of the International Conference on Software Engineering (ICSE), 2021.
