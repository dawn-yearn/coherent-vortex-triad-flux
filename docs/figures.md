# Figure sources

[Return to the discovery note](../README.md)

Both figures are newly drawn for this package. They use the parent project's shared `paper_style` (white background, serif/STIX typography, blue #0072B2, green #009E73, vermilion #D55E00, signed RdBu_r fields). The exact style module is preserved in [scripts/paper_style.py](../scripts/paper_style.py); its SHA-256 appears in the [source manifest](../evidence/source_manifest.json).

## Mechanism

The field is the analytic background $\psi=\omega=\cos x+\cos y$ at $A=1$. Streamlines use $u=(\partial_y\psi,-\partial_x\psi)$, consistent with $\omega=-\Delta\psi$. This illustrates the prescribed model, not a turbulent DNS field.

The Fourier plot uses the certified 62-mode set. Colors and marker shapes show first arrival at depths 0–3. Lines denote nonzero background coupling, not flux magnitude or a unique causal path.

Signed bars use exact rational centers from [mechanism.json](../evidence/mechanism.json). Their certified radii are below 0.004779 in the plotted $10^{-6}$ units, smaller than the line width. The zero-centered unlisted remainder is bounded explicitly.

## Convergence

Points show certified relative-error **upper** bounds. A separate **lower** bound proves depth 2 fails: its negative-channel discrepancy exceeds 5.126427%. An upper bound exceeding 5% would not by itself prove failure.

## Rebuild

From the repository root, with NumPy and Matplotlib installed:

```sh
python scripts/make_figures.py
```

The script regenerates [summary.json](../data/summary.json) and PNG/SVG figures. Rounded plotting data do not replace exact fractions for acceptance. Rendering dependencies are listed in [requirements-render.txt](../requirements-render.txt); the arithmetic checker needs only the Python standard library.

The organization was inspired by [Ericksen-complete](https://github.com/Jingbei-Bai/Ericksen-complete): a concise discovery narrative, figures, downloadable note, and detailed evidence on separate pages. No scientific content, image, code or license from that repository is reused.
