# BERT-Duplicate-Bug-Report-Detection

This repository contains source code for research on Duplicate Bug Report Detection using Siamese BERT-Networks. 

### Duplicate Bug Report Detection Siamese BERT Model

For the model itself and its training/validation pipeline refer to **dbrd.jpynb** notebook file.

To launch the notbeook locally run the following commands:
```
pip install jupyterlab
```
```
jupyter-notebook .\dbrd.ipynb
```

The notebook can also be found on Google Colab:
https://colab.research.google.com/drive/1VxxCeB61fPAQu9VjkRyO_6UC_a4AprkR?usp=sharing

Example model fine-tuned on 40000 Open Office project pairs can be found on:
https://drive.google.com/drive/folders/1Irhm1B05Yj-gD0hKf_RtyD-XBauYLVMN?usp=sharing

### Data for Training and Validation

Bug datasets for training/validation are taken from: 
http://alazar.people.ysu.edu/msr14data/

This contains MongoDB dumps in .bson format that can later on be consumed by the helper scripts to prepare the data for the model.

#### bson_to_csv_issues_utility.py

Parses bson dump file of bugs dataset, preprocesses it and returns a csv file of all the issues in the dataset.

Example use: 
```
python .\bson_to_csv_issues_utility.py --input ooall.bson --output ooall.csv
```

### pairs_generator_csv.py

Generates bug description pairs for model fine-tuning. Can be configured by tweaking constants within the script:
- **ISSUES_FILE** - source for the generated csv file containing all of the issues
- **GENERATED_PAIRS_FILE** - output csv file that will contain the generated pairs
- **PAIRS_COUNT** - the number of pairs to be generated
- **DUPLICATE_PAIRS_RATIO** - the part of duplicate pairs within all of the pairs
- **PART_TO_USE_FOR_GENERATION** - the part of original issues to be used for pair generation (we want to exclude the most recent issues for validation, for example)

Example use:
```
python .\pairs_generator_csv.py
```
