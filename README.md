# EE 541 HW9
Author: Quanhao Sun
Student ID: 5579191857

## Contents

Submit **README.md** (this file) plus everything under **`q1/`**. Raw images stay in `S1_Raw_Photographs_Full_Study/` at the HW9 root; run `python q1/prepare_data.py` or open the notebook with working directory **`HW9/q1`** so outputs land in `q1/`.

q1/
└── EE541_HW9.ipynb                    # full pipeline: splits, training, curves, confusion matrix, PR curves, feature maps, baseline comparison
└── prepare_data.py                    # builds data/{ethanol,pentane,propanol}/ and prepared_data/{train,val,test}/ (70/15/15, seed 42)
└── hw9_learning_curves.png
└── hw9_confusion_matrix.png
└── hw9_precision_recall.png
└── hw9_features_conv1.png
└── hw9_features_layer2b0_conv1.png
└── hw9_features_layer3b0_conv1.png
