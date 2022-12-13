from .cython_wrapper import ils_spread
from .admm import admm
from numpy import array, split, argmin, intc, empty_like, arange, argsort
from scipy.ndimage.filters import gaussian_filter1d

class ILS():

    def __init__(self, ):
        self.rmin = None

    def label_spreading(self, X, indx_labelled = [0], labels = [1]):
        # todo: decide how to pick the first point

        self._X = X;
        self.n_labelled = len(indx_labelled)
        
        X_flat = X.flatten()

        self.dims = X.shape[1]
        self.n_points = X.shape[0]
        
        unlabelled_inds = [i for i in range(self.n_points) if i not in indx_labelled]

        labelled = array(indx_labelled, dtype= intc)
        unlabelled = array(unlabelled_inds, dtype=intc)
        labels = array(labels, dtype=intc)

        temp_labels, temp_ords, temp_rmin = ils_spread(labelled,
                unlabelled, X_flat, labels, self.dims, 
                self.n_points, self.n_labelled)
        if len(indx_labelled) == 1:
            # don't set rmin if the this is the second spreading call
            self.rmin = temp_rmin
            self.ordering = temp_ords
        else:
            self.labels = list(array(list(labels) + temp_labels)[invert_permutation(indx_labelled + temp_ords)])


    def segmentation(self, inds):
        
        if self.rmin is None:
            raise Exception("Perform label spreading before segmentation or pass custom rmin")

        segments = split(self.rmin, inds)
        segmented_ords = split(self.ordering, inds)
        segment_sm = [gaussian_filter1d(seg, max(5, len(seg)//10)) for seg in segments]
        mins = [ords[argmin(seg)] for (seg, ords) in zip(segment_sm, segmented_ords)]

        labels = [i+1 for i in range(len(mins))]

        return mins, labels



        


def invert_permutation(p: list):
    '''
    This inversino func was taken from stack exchange
    https://stackoverflow.com/a/25535723
    By user 'Ali'
    Thanks!
    '''
    inv = empty_like(p)
    inv[p] = arange(len(p))

    return list(inv)
