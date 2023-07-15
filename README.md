# iterLS: An Implementation of Iterative Label Spreading

This is an implementation of a semi-supervised/unsupervised clustering method called Iterative Label Spreading. The main algorithm is written in c, and wrapped in cython for use in python. The algorithm is presented in the following paper by Amanda J. Parker and Amanda S. Barnard. 

"Selecting Appropriate Clustering Methods for Materials Science Applications of Machine Learning". Published 09/10/2019. 
DOI:  https://doi.org/10.1002/adts.201900145

To use the algorithm, I recommend reading the paper first as it describes how to use Iterative Label Spreading. Use cases go beyond simple clustering such as evaluating performance of a given clustering on a data set. 

The current implementation is very minimal, providing methods and variables that should allow the user, with plotting techniques, to use Iterative Label Spreading effectively. Plotting techniques and suggested segmentation is on my todo list. Currently, I have not rigoroursly tested edge cases, feel free to raise an issue or pull request.

## Installation

```bash
git clone git+https://github.com/Dan-Tan/Iterative-Label-Spreading.git
cd Iterative-Label-Spreading
pip install .
```

## Usage

For more examples with plots see [notebooks](https://github.com/Dan-Tan/Iterative-Label-Spreading/blob/master/notebooks/Example_Usage.ipynb)

```python
from iterLS import ILS

data_set # 2-D numpy array of shape (n_points, dimensions)

example_ILS = ILS()
example_ILS.label_spreading(data_set)

segmentation_indices = [...] # pass in indices you wish to segment rmin 
indices, labels = example_ILS.segmentation(segmentation_indices)

example_ILS.label_spreading(data_set, indices, labels) # final label Spreading

example_ILS.labels # final label result for entire dataset
example_ILS.rmin # list of distances returned from label spreading
```

If you have any issues with install feel free to raise and issue.

## Todo:

* Add tests
* Document code
* Add additional plotting methods to aid with viewing results, segmentation and general QOL
* Implementation reliable auto-segmentation method


