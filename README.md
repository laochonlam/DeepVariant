# Deep Variant


## Introduction
Implementation of ***Finding candidate variants*** and ***Creating images around candidate variants*** sections in [Google Variant Caller Paper](http://www.biorxiv.org/content/early/2016/12/14/092890).

Run ```run.sh``` to find candidate variants, then generate 3 types of images which are ***ref***, ***het*** and ***hom-alt*** for further CNN training network by given a specific range.


## Structure
- find_candidate
    - find.py
    - find_candidate.sh
- image_generation
    - draw.py
    - gen_image.py
- label_classification
    - label_classification.py
- tools
    - samtools-1.5/
    - image_count.sh
    - run_sample.sh
- run.sh

```find_candidate.sh``` - select the following 1000000 position to find candidate.

```find.py``` - find candidate.

``` draw.py``` - draw image with feature.

```gen_image.py``` - preprocessing of image drawing.

```label_classification.py``` classify those images into ***ref***, ***het*** and ***hom-alt*** then call image generation script.

```samtools1.5/``` - samtools.

```image_count.sh``` - count image in each class.

```run_sample.sh``` - sample script for understanding how to run.

## Usage
```
Usage: run.sh <chr> <start pos> <end pos>
```
sample run script can be found in ```tools/run_sample.sh```.
