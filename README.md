# iterLS: An Implementation of Iterative LabelhSpreading

This is an implementation of a semi-supervised/unsupervised clustering methods called Iterative Label Spreading. The algorithm is presented in the following paper by Amanda J. Parker and Amanda J. Barnard. 

"Selecting Appropriate Clustering Methods for Materials Science Applications of Machine Learning". Published 09/10/2019. 
DOI:  https://doi.org/10.1002/adts.201900145

To use the algorithm, I recommend reading the paper first as it describes how to use Iterative Label Spreading, as use cases go beyond simple clustering such as evaluating performance of a given clustering on a data set. 

The current implementation is very minimal however provides methods and variables that should allow the user, with plotting techniques, to use Iterative Label Spreading effectively. Providing plotting techniques and suggested segmentation is on my todo list. Currently, I have not rigoroursly tested edge cases, feel free to raise an issue or pull request.

## Installation

```bash
git clone
cd iterLS
pip install -e .
```

## Usage

```python
from iterLS import ILS

data_set # 2-D numpy array of shape (n_points, dimensions)

example_ILS = ILS()
example_ILS.label_spreading(data_set)

segmentation_indices = [...] # pass in indices you wish to segments rmin 
indices, labels = example_ILS.segmentation(segmentation_indices)

example_ILS.label_spreading(data_set, indices, Label) # final label Spreading

example_ILS.labels # final label result for entire dataset
example_ILS.rmin # list of distances returned from label spreading
```

## Todo:

* Add tests
* Document code
* Add additional plotting methods to aid with viewing results, segmentation and general QOL
* Implementation reliable auto-segmentation method


