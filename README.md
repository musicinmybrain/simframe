# Simframe

[![Documentation Status](https://readthedocs.org/projects/simframe/badge/?version=latest)](https://simframe.readthedocs.io/en/latest/?badge=latest) [![GitHub](https://img.shields.io/github/license/stammler/simframe) ](https://github.com/stammler/simframe/blob/master/LICENSE) [![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/stammler/simframe/blob/master/.github/CODE_OF_CONDUCT.md)  
[![status](https://joss.theoj.org/papers/0ef61e034c57445e846b2ec383c920a6/status.svg)](https://joss.theoj.org/papers/0ef61e034c57445e846b2ec383c920a6)  
[![PyPI - Downloads](https://img.shields.io/pypi/dm/simframe?label=PyPI%20downloads)](https://pypistats.org/packages/simframe) [![Fedora package](https://img.shields.io/fedora/v/python3-simframe?color=blue&label=Fedora%20Linux&logo=fedora)](https://src.fedoraproject.org/rpms/python-simframe)

### Framework for scientific simulations

`Simframe` is a Python framework to facilitate scientific simulations. The scope of the software is to provide a framework which can hold data fields, which can be used to integrate differential equations, and which can read and write data files.

Data fields are stored in modified `numpy.ndarray`s. Therefore, `Simframe` can only work with data, that can be stored in `NumPy` arrays.

## Installation

`pip install simframe`

## Documentation

[https://simframe.readthedocs.io/](https://simframe.readthedocs.io/)

* [1. Simple Integration](https://simframe.readthedocs.io/en/latest/1_simple_integration.html)
* [2. Advanced Integration](https://simframe.readthedocs.io/en/latest/2_advanced_integration.html)
* [3. Updating Groups and Fields](https://simframe.readthedocs.io/en/latest/3_updating.html)
* [4. Custom Integration Schemes](https://simframe.readthedocs.io/en/latest/4_custom_schemes.html)
* [5. Adaptive Integration Schemes](https://simframe.readthedocs.io/en/latest/5_adaptive_schemes.html)
* [6. Implicit Integration](https://simframe.readthedocs.io/en/latest/6_implicit_integration.html) <br /> &nbsp;
* [Example: Coupled Oscillators](https://simframe.readthedocs.io/en/latest/example_coupled_oscillators.html)
* [Example: Double Pendulum](https://simframe.readthedocs.io/en/latest/example_double_pendulum.html)
* [Example: Compartmental Models](https://simframe.readthedocs.io/en/latest/example_compartmental_models.html)
* [Example: N-body Problem](https://simframe.readthedocs.io/en/latest/example_nbody.html) <br /> &nbsp;
* [A. Citation](https://simframe.readthedocs.io/en/latest/A_citation.html)
* [B. Contributing/Bugs/Features](https://simframe.readthedocs.io/en/latest/B_contrib_bug_feature.html)
* [C. Changelog](https://simframe.readthedocs.io/en/latest/C_changelog.html) <br /> &nbsp;
* [Module Reference](https://simframe.readthedocs.io/en/latest/api.html)

## Ackowledgements

`simframe` has received funding from the European Research Council (ERC) under the European Union’s Horizon 2020 research and innovation programme under grant agreement No 714769.

`simframe` was developed at the [University Observatory](https://www.usm.uni-muenchen.de/index_en.php) of the [Ludwig Maximilian University of Munich](https://www.en.uni-muenchen.de/index.html).
