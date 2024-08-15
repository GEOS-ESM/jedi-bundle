# Building JEDI code on Discover (SLES 12)

1) Load the JEDI spack Python modules (These modules will load Python version 3.9):

``` bash
module purge
module load git git-lfs
module use /discover/swdev/jcsda/spack-stack/modulefiles
module load miniconda/3.9.7
```

2) Load the latest `jedi_bundle` module:

``` bash
module use -a /discover/nobackup/projects/gmao/advda/JediOpt/modulefiles/core/
module load jedi_bundle
```

3) Create a directory where the source code and build directory will be stored e.g.:

``` bash
mkdir jedi-work
cd jedi-work
```

4) Issue `jedi_bundle` without any arguments to generate the `build.yaml` configuration:

``` bash
jedi_bundle
```

Before proceeding you may want to edit `build.yaml` to choose different options. It will default to building all bundles and you may wish to only build a specific bundle by modifying `clone_options.bundles`. Choosing `fv3-jedi` and `ufo`, for example, will result in building all the code for the `fv3-jedi` and `ufo` bundles. You may also want to change the modules used to build or change the type of build to use.

Once `build.yaml` is configured they way you wish, you can issue `jedi_bundle` again with the tasks you want. 

5) Clone & configure the JEDI repositories on a login node (clone & configure arguments can be issued seperately):

``` bash
jedi_bundle clone configure build.yaml
```

6) Then proceed building JEDI using a compute node. First, request interactive nodes with the following:

``` bash
salloc --time=1:00:00
```
To ensure proper modules and `jedi_bundle` is loaded, repeat steps 1 and 2. Then build the bundle via:

``` bash
jedi_bundle make build.yaml
```

Note that you may wish to perform the make step using more than the default 6 cores. Edit `build.yaml` and change `make_options.cores_to_use_for_make` to a higher number, say 24 and then issue the `jedi_bundle make build.yaml` step again after requising the node(s) with `salloc`.
