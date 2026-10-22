# Evidence and verification

[Discovery note](../README.md) · [Mathematical contract](../docs/mathematics.md)

This is a compact discovery package. It exports selected exact certificates, including the independently computed sign and 62-mode certificates. The source JSON files and baseline checker are byte-for-byte copies of the frozen Phase08 records. [source_manifest.json](source_manifest.json) identifies the source study, source filename and SHA-256.

## What is included

| Record | Role |
| :--- | :--- |
| [full_certificate.json](full_certificate.json) | Infinite-lattice rational center, endpoints and separate error budgets |
| [full_independent.json](full_independent.json) | Independently computed sign certificate |
| [mechanism.json](mechanism.json) | Connected/mean decomposition, exact orbit masks and 457 orbit records |
| [sideband_0.json](sideband_0.json) – [sideband_3.json](sideband_3.json) | Four model families, exact mode sets and five target comparisons |
| [sideband_independent.json](sideband_independent.json) | Independent 62-mode result |
| [baseline.json](baseline.json) | Finite Fourier/Wick checks and exact unmodulated baseline |

## Run the lightweight check

Python 3.10+; no third-party packages:

```sh
python scripts/verify.py
```

The checker replays the original baseline, recomputes the rational error-budget sum and outward enclosures, reconciles connected/mean and signed-mask identities, reconstructs the 6/20/38/62 mode family, recomputes relative-error upper/lower bounds, compares the independent records and checks exported hashes.

It does **not** regenerate the 114,079-orbit infinite-lattice candidate or its full nonlinear residual, nor machine-check the analytic semigroup proof. Those computations were completed and independently challenged in the archived research runs. A complete solver rerun would require the larger candidate/source archive; the verification scope here is explicit so that a successful lightweight check is not confused with a fresh end-to-end proof.

Each exploratory numerical command in the underlying work had a 60-second limit. The export check and figure rendering also use bounded local runs; there is no training or DNS simulation.

## Rebuild the presentation

```sh
python scripts/make_figures.py
python scripts/make_pdf.py
```

These require the optional dependencies in [requirements-render.txt](../requirements-render.txt). The PDF script uses built-in ReportLab fonts and the generated formula images, so no TeX installation or platform-specific font path is needed. The document has three explicitly composed pages.

The analytical scope is the normalized leading three-fluctuation flux at the fixed test point. The 62-mode minimality statement applies only to the declared nested family and the five-target, 5% rule. No DNS population result, universal SGS impossibility theorem or proof-kernel formalization is claimed.
