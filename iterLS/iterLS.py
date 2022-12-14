from .cython_wrapper import ils_spread
from .admm import admm
from numpy import array, split, argmin, intc, empty_like, arange, argsort

class ILS():

    def __init__(self, ):
        self.rmin = None

    def label_spreading(self, X, indx_labelled = [0], labels = [1]):
        '''
        Takes a data set the index of the starting point/s and label/s. 
        If using for unsupervised learning passing a starting point is optional.
        Arguements:
            X: numpy array (number of points, dimensions), data set
            indx_labelled: list of integers indexing X for starting points
            labels: list of integers, labels fof starting points
        Returns:
            void

        Results are stored in self.rmin, self.ordering or self.labels
        Read README for instructions on how to use. 
        '''
        # flatten returns a copy
        X_flat = X.flatten()

        self.dims = X.shape[1]
        self.n_points = X.shape[0]
        
        unlabelled_inds = [i for i in range(self.n_points) if i not in indx_labelled]
        
        # convert  integers to 32 bit integers (c integers)
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
            #  re-order labels to match the order of the data set 
            self.labels = list(array(list(labels) + temp_labels)[invert_permutation(indx_labelled + temp_ords)])


    def segmentation(self, inds):
        '''
        Only call this function if rmin has been initialised via label spreading
        with one initial point. 

        Arguements:
            inds: list of integers to segment rmin
        Returns:
            mins: list of integers indexing starting points
            labels: list of integers, labels of starting points
        '''
        
        if self.rmin is None:
            raise Exception("Perform label spreading before segmentation")
        
        # split rmin and ordering according to the indices passed
        segments = split(self.rmin, inds)
        segmented_ords = split(self.ordering, inds)
        
        # smooth rmin using ADMM total variation noise reduction
        segment_sm = [admm(seg, 20, 100, 5) for seg in segments]

        # find minimum of the smoothed segments (points of minimum density)
        mins = [ords[argmin(seg)] for (seg, ords) in zip(segment_sm, segmented_ords)]
        
        # initialise the labels for the starting points
        labels = [i+1 for i in range(len(mins))]

        return mins, labels


def invert_permutation(p: list):
    '''
    This inverion function was taken from stack exchange
    https://stackoverflow.com/a/25535723
    By user 'Ali'
    Faster than using argsort as sorting is not required. 
    Thanks!

    Function computes the inverse of a given permutation. 
    '''
    inv = empty_like(p)
    inv[p] = arange(len(p))

    return list(inv)
