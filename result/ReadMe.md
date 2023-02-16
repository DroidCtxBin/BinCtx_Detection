# Evaluation
## Overall Effectiveness
As shown in Table 4 (below), BinCtx effectively identifies and classifies malicious apps and undesired behavior with an average precision of 94.01%. Compared
with existing works, BinCtx achieves a performance improvement of at least 17.66% on average.
![image](https://github.com/DroidCtxBin/BinCtx_Detection/blob/main/result/overall_result.png)

As shown in Table 5 and 6, each feature is essential for BinCtx to effectively identify undesired/malicious behaviors. 
![image](https://github.com/DroidCtxBin/BinCtx_Detection/blob/main/result/feature_importance.png)
![image](https://github.com/DroidCtxBin/BinCtx_Detection/blob/main/result/BinCtx_vs_bytecode.png)
The importance values of each feature is measured by permutation feature importance. The basic logic is to randomly shuffle each feature at a time to break the relationship between the features and the target (label), and thus drop the model score is indicative of how much of the model depend on the feature. In our study, we use the drop of model's accuracy to measure the permutation importance value, i.e. $original\_model\_accuracy - shuffle\_model\_accuracy$.

Among three features extracted, the bytecode of an app is the most important one, followed by the usage pattern of 3rd-party library, and contextual information such as intent actions and URL constants.
