# Geospatial data processing with Kedro

## Overview

This demos shows how to use kedro with geospatial data. Uses the wip implementation of raster dataset from
the [kedro-datasets](https://github.com/kedro-org/kedro-plugins/pull/355) PRs

Take a look at the [Kedro documentation](https://docs.kedro.org) to get started.

### Rules and guidelines kedro suggests and we endorse:

* Don't remove any lines from the `.gitignore` file we provide
* Make sure your results can be reproduced by following
  a [data engineering convention](https://docs.kedro.org/en/stable/faq/faq.html#what-is-data-engineering-convention)
* Don't commit data to your repository
* Don't commit any credentials or your local configuration to your repository. Keep all your credentials and local
  configuration in `conf/local/`

## How to install dependencies

```
pip install -r requirements.txt
```

## How to run the pipelines

```
kedro run
```

## How to visualize the pipeline

```
kedro viz run 
``` 

## How to test the project

simply:

```
pytest
```

To configure the coverage threshold, look at the `.coveragerc` file.

## How to work with Kedro and notebooks

> Note: Using `kedro jupyter` or `kedro ipython` to run your notebook provides these variables in
> scope: `catalog`, `context`, `pipelines` and `session`.
>
> Jupyter, JupyterLab, and IPython are already included in the project requirements by default, so once you have
> run `pip install -r requirements.txt` you will not need to take any extra steps before you use them.

### Jupyter

To use Jupyter notebooks in your Kedro project, you need to install Jupyter:

```
pip install jupyter
```

After installing Jupyter, you can start a local notebook server:

```
kedro jupyter notebook
```

### JupyterLab

To use JupyterLab, you need to install it:

```
pip install jupyterlab
```

You can also start JupyterLab:

```
kedro jupyter lab
```

### IPython

And if you want to run an IPython session:

```
kedro ipython
```