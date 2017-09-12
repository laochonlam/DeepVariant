# Deep Variant

## File Structure
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