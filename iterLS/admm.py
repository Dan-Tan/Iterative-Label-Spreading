from scipy.sparse.linalg import cg
from scipy.sparse import diags, identity
from numpy import array, zeros, eye, reshape, matmul, abs, maximum, sign

def admm(b, alpha, t, iters = 100):
    
    n = len(b)
    b = array(b).reshape((-1, 1))
    diag = [[-1 for i in range(n-1)], [1 for i in range(1)]]
    D = diags(diag, [0, 1], shape = (n-1, n))

    lambda_k = zeros((n-1, 1))
    z_k = zeros((n-1, 1))
    
    # avoid repeated computations in the loop
    A = identity(n) + t * (D.transpose()).dot(D)
    DT = D.transpose()
    
    for i in range(iters):
        # D is a very sparse matrix, so conjugate gradient is quite quick
        x_k, _ = cg(A, t * DT.dot(z_k) - DT.dot(lambda_k) + b)
        x_k = x_k.reshape((-1, 1))
        Dx = D.dot(x_k) #avoid recomputation
        z_k = S(Dx + 1/t * lambda_k, alpha/t)
        lambda_k = lambda_k + t * (Dx  - z_k)

    return list(x_k.flatten())

def S(x, t):
    return sign(x) * maximum(abs(x) - t, 0)

