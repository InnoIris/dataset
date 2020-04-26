# Dataset repository for InnoIris

This code repository contains the dataset that we used while developing InnoIris.

This code also contains all the tools to generate and organise the dataset properly.

### Development Guide

In order to start using this in the server there are a few steps that need to be followed.

If you have a custom dataset, make sure to put it in the `custom dataset` folder, under the right class name folder.

Then you must run the `custom_dataset_parser.py` script in order to make the Imagenet completely combined with your custom dataset.

```
python custom_dataset_parser.py
```

To generate the label csv files for training, you must run the `parser.py` script.

```
python parser.py
```

The dataset is ready for training!
