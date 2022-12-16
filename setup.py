from setuptools import setup, find_packages, Extension
import numpy as np

from Cython.Build import cythonize

if __name__ == "__main__":
    extensions = cythonize(
            Extension(
                name = "iterLS.cython_wrapper",
                sources = ["iterLS/cython_wrapper.pyx", 'iterLS/label_spreading.c', "iterLS/convert.c", "iterLS/node_structure.c"],
                include_dirs = ["iterLS"],
                extra_link_args = ["-lm"],
                language = 'c'
                ),
        compiler_directives={'language_level': 3},
        annotate=True)

    setup(
        use_scm_version={"version_scheme": "no-guess-dev"},
        name='iterLS',
        version='0.1.0',
        include_dirs = [np.get_include(), "iterLS"],
        package_data={"iterLS": ["*.pyx", "*.c", "*.h", "*.py"]},
        setup_requires=['Cython', 'numpy', 'scipy', 'matplotlib', 'scikit-learn'],
        packages = ['iterLS'],
        install_requires = ['numpy', 'scipy', 'Cython', 'matplotlib', 'scikit-learn'],
        ext_modules=extensions
        )
