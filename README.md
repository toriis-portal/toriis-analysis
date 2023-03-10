[![analysis-notebook-test-binder](https://github.com/toriis-portal/toriis-analysis/actions/workflows/analysis-notebook-test-binder.yml/badge.svg)](https://github.com/toriis-portal/toriis-analysis/actions/workflows/analysis-notebook-test-binder.yml)
# toriis-analysis
Repository for scripts to evaluate public institutional investment data. These scripts are designed to be launched with [binder](https://mybinder.org/) so that other community members can run their own analyses without any additional setup.



[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/toriis-portal/toriis-analysis/HEAD)

# Running existing notebook

1. **Interactive, UI-only:** Launch the repo in binder and clone one of the example notebooks
1. **Interactive, CLI only:** 
	1. Fork + clone repo
	1. Run `setup/setup.sh` to set up the local conda environment
		- you may need to install the correct version of miniconda
	1. Start a local notebook suerver (`juypter notebook`)

# Contributing

You are welcome to contribute data and analysis results. Please make sure that you contribute **cleared notebooks** so version control capabilities work well. To clear a notebook, use `Kernel -> Researt & Clear Output)` 

1. **UI-only:**
    1. Download the notebook (Download -> ipynb)
    1. Upload the notebook using the GitHub UI (Upload Files, next to Clone or Download)
1. **CLI only:** Follow the [instructions on github](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) - i.e.
    1. Create a new branch (e.g. `$ git checkout -b`)
    1. Commit the new notebook (e.g. `$ git add` and `$ git commit`)
    1. Push and generate pull request 

