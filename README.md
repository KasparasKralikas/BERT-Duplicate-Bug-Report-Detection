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

Install requirements before using the utility scripts:
```
 pip install -r .\requirements.txt
```

#### bson_to_csv_issues_utility.py

Parses bson dump file of bugs dataset, preprocesses it and returns a csv file of all the issues in the dataset.

Example use: 
```
python .\bson_to_csv_issues_utility.py --input ooall.bson --output ooall.csv
```

#### pairs_generator_csv.py

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

### dbrd_web_api.py - Web API for retrieving top-K similar bug reports via Fine-tuned model

Flask server that provides endpoint for retrieving top-K similar bug reports to the given textual description of a bug report.

This requires a pre-trained model (refer to Duplicate Bug Report Detection Siamese BERT Model section) which is specified by **MODEL_PATH** constant within the script.

It also requires a list of issues (bug reports) from which we will retrieve the top-K similar ones. Issues file is specified with **ISSUES_FILE** constant within the script. It is expected that each issue will contain *bug_id*, *short_desc* and *description* properties. Example list of Open Office issues can be found on:
https://drive.google.com/file/d/1O1lDUC_LeYidsN6Hy17V38WdxLq5LT6O/view?usp=sharing

On startup, embeddings (vector representations of bug reports) are calculated and stored in a file specified by **EMBEDDINGS_OUTPUT** constant within the script. That way if server needs to be restarted, same embeddings can be reused to avoid expensive and time consuming computations.

Install requirements before launching the server:
```
 pip install -r .\requirements.txt
```
Then run the following command:
```
 python .\dbrd_web_api.py
```

This should start the server on a local machine listening on port 5000. 

Retrieve top-K similar issues for the given issue description:
- POST: localhost:5000/retrieve_duplicates

Requires JSON body with *description* and *top_k* properties:
```
{
    "description": "Bug report description",
    "top_k": 25
}
```

Example response:
```
{
    "similar_issues": [
        {
            "description": "Bug report description that's the most similar to the given description",
            "id": 10001,
            "similarity": 0.95
        },
        {
            "description": "Bug report description that's the second most similar to the given description",
            "id": 10003,
            "similarity": 0.92
        },
        ...
}
```

### Author

**Kasparas Kralikas**

* [github](https://github.com/KasparasKralikas)
* [linkedin](https://www.linkedin.com/in/kasparas-kralikas-905848156/)

### License

Copyright © 2021, [Kasparas Kralikas](https://github.com/KasparasKralikas).
Released under the [MIT License](LICENSE).
