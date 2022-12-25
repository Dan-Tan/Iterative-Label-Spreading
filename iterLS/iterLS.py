from .cython_wrapper/cython_wrapper import ils_spread
from .admm import admm
from numpy import array, split, argmin, intc, empty_like, arange, argsort, zeros, hstack

# used for plotting methods
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

# dimensionality reduction
from sklearn.manifold import TSNE

class ILS():

    def __init__(self, ):
        self.rmin = None
        self._embedding = None;

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
        self._X = X
        X_flat = X.flatten()

        self.dims = X.shape[1]
        self.n_points = X.shape[0]
        n_labelled = len(indx_labelled)
        
        unlabelled_inds = [i for i in range(self.n_points) if i not in indx_labelled]
        
        # convert  integers to 32 bit integers (c integers)
        labelled = array(indx_labelled, dtype= intc)
        unlabelled = array(unlabelled_inds, dtype=intc)
        labels = array(labels, dtype=intc)
        
        temp_labels, temp_ords, temp_rmin = ils_spread(labelled,
                unlabelled, X_flat, labels, self.dims, 
                self.n_points, n_labelled)

        if len(indx_labelled) == 1:
            # don't set rmin if the this is the second spreading call
            self.rmin = temp_rmin
            self.ordering = temp_ords
            self._first = indx_labelled
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

    def plot_rmin(self, cluster_colouring = False, labels = None, colours = plt.cm.tab20, max_rmin = None):
        '''
        Plot the distance ILS 'jumped' each iterations with the option to include colouring by cluster_colouring
        and providing labels if evaluating cluster quality. 
        Arguements:
            cluster_colouring: Boolean (default: False), colour plot by clusters (True)
            labels: (optional) labels for each iteration (one less then number of non labelled)
            colours: matplotlib.pyplot colourmap
            max_rmin: double, maximum of the y-axis
        Returns:
            void
        '''

        if self.rmin is None:
            raise Exception("Rmin not initialised, run label spreading before this function call")
        
        if not cluster_colouring:
            labels = [1 for i in range(self.n_points)]
        elif labels is None and self.labels is None:
            raise Exception("No labels initialised or passed")
        elif labels is None:
            labels = self.labels
        
        n_clusters = len(set(labels))
        label_permuted = [labels[i] for i in (self.ordering)]

        # create line segments for LineCollection to speed up plotting
        temp = array([[xi, yi] for (xi, yi) in zip(arange(len(self.rmin)), self.rmin)])
        temp = temp.reshape((-1, 1, 2))
        segments = hstack([temp[:-1], temp[1:]])
        
        fig, ax = plt.subplots()
        ymax = max(self.rmin) if max_rmin is None else max_rmin
        ax.set_xlim([0, len(self.rmin)])
        ax.set_ylim([0, ymax])

        colours = [colours(label_permuted[i]) for i in range(len(self.rmin))]
        lineColl = LineCollection(segments, colors = colours, linestyle='solid')

        ax.add_collection(lineColl)
        cond_title = "Coloured by Clusters" if cluster_colouring else ""
        ax.set_title(r"$R_{min}$ Plot " + cond_title)
        ax.set_ylabel(r"$R_{min}$")
        ax.set_xlabel("ILS ordering")
        plt.show()

    def plot_ordering(self, colours = 'spring', X = None, size = 1, use_embedding = False, path = None, *args, **kwargs):
        '''
        plot the ordering of ILS through the data. For high dimensional data use t-SNE or pass
        data set with dimensionsality reduction to 2D

        Arguements:
            colours: matplotlib continuous colour map
            X: (optional) data set passed; default is set used originally
            size: size of scatter points
            use_embedding: Boolean, use an embedding previously stored in ILS.
            *args, **kwargs: params for tSNE
        Return:
            void
        '''

        if X is None and self._X is None:
            raise Exception("Data not given or initialised, run label spreading before this function call")
        elif X is None:
            X = self._X

        dims = X.shape[0]

        if dims != 2:
            # performs TSNE here
            if self._embedding is None and X is None and (not use_embedding):
                raise Exception("Not embedding given, requested or stored. Try use_embedding = True or pass an embedding")
            if not use_embedding:
                self._embedding = TSNE(*args, **kwargs).fit(self._X.copy()).embedding_
            if self._embedding.shape[1] != 2:
                raise Exception("Dimensions of t-SNE embedding should be 2")
        
        c_ords = self._first + self.ordering
        plt.scatter(X[c_ords, 0], X[c_ords, 1], c = arange(self.n_points), cmap = colours, s = size)
        if path is not None:
            plt.savefig(path)
        else:
            plt.show()

    def plot_labels(self, colours = 'spring', X = None, size = 1, use_embedding = None, path = None, *args, **kwargs):
        '''
        Plot the labels given by ILS. For higher dimensionsal data use 
        t-SNE or pass data set with dimensionsality to 2D.
        Arguements:
            colours: String, name of continuous colour map given or list of colours
            X: (Optional), given dataset of dimensions 2 default is data set used for label spreading
            size: int (default = 1), size of points on the scatter plot
            *args, **kwargs: arguements to be passed to t-SNE
        Return: 
            void
        '''

        if X is None and self._X is None:
            raise Exception("Data not given or initialised, run label spreading before this function call")
        elif X is None:
            X = self._X
        
        dims = X.shape[0]
        if dims != 2:
            # performs TSNE here
            if self._embedding is None and X is None and (not use_embedding):
                raise Exception("Not embedding given, requested or stored. Try use_embedding = True or pass an embedding")
            if not use_embedding:
                self._embedding = TSNE(*args, **kwargs).fit(self._X.copy()).embedding_
            if self._embedding.shape[1] != 2:
                raise Exception("Dimensions of t-SNE embedding should be 2")

        if (not isinstance(colours, list)):
            n_clusters = len(set(self.labels))
            cmap = plt.get_cmap(colours)
            colours = [cmap(lab/n_clusters) for lab in self.labels]

        plt.scatter(X[:, 0], X[:, 1], c = colours, s = size)

        if path is not None:
            plt.savefig(path)
        else:
            plt.show()



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
