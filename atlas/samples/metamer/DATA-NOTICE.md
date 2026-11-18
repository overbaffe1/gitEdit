# Spectral reference data

`standards.json` contains a numerical subset selected from **colour-science/colour** at commit `6c3daee61532ec68d3c89bd203cb99d97baadf28`:

- [CIE 1931 2° XYZ colour matching functions](https://github.com/colour-science/colour/blob/6c3daee61532ec68d3c89bd203cb99d97baadf28/colour/colorimetry/datasets/cmfs.py), key `CIE 1931 2 Degree Standard Observer` in `DATA_CMFS_STANDARD_OBSERVER`.
- [D65 and A illuminants](https://github.com/colour-science/colour/blob/6c3daee61532ec68d3c89bd203cb99d97baadf28/colour/colorimetry/datasets/illuminants/sds.py), keys `D65` and `A` in `DATA_ILLUMINANTS_CIE`.
- [Bradford matrix reference](https://github.com/colour-science/colour/blob/6c3daee61532ec68d3c89bd203cb99d97baadf28/colour/adaptation/datasets/cat.py).

Selection: 380–780 nm inclusive at 5 nm intervals, 81 rows. Numeric literals were extracted with Python AST and `ast.literal_eval`; the downloaded package code was not executed or installed. No interpolation was required for these selected wavelengths. This is a local educational selection, not an independently downloaded or certified CIE publication. See the upstream dataset source headers for their bibliographic references.

**Copyright 2013 Colour Developers.** The upstream [BSD-3-Clause license](COLOUR-LICENSE.txt) is retained verbatim. Derived CSV and embedded browser data carry the same attribution through `atlas/metamer.md`, this notice and the accompanying license. Both `assets/metamer/COLOUR-LICENSE.txt` and the license inside `bench.zip` reproduce that notice and its full terms. No endorsement by Colour Developers or CIE is implied.

Reflectance curves A/B, the nullspace search, the colour computations, the plots and the browser UI are original to this exhibit. No measured pigment data or external artwork is included. The rest of the screened projects supplied ideas and scope comparisons, not copied implementation code.
