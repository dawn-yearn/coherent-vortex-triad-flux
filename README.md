# How a coherent vortex reshapes triad energy transfer

**Phase08 · A certified mechanism in two-dimensional Navier–Stokes fluctuations**

[中文介绍](README.zh-CN.md) · [3-page discovery note](discovery-note.pdf) · [Mathematical details](docs/mathematics.md) · [Evidence & verification](evidence/README.md)

An order-one cellular vortex weakens a negative triad-flux coefficient by **10.77%**. More than **99.43% of the change is connected third-order response**, rather than an induced-mean contribution. Recovering this effect requires resolving both the original triad and the opposing channels created around it.

<img src="assets/mechanism.png" width="980" alt="Analytic cellular vortex, its 62-mode Fourier sideband neighborhood, and opposing positive and negative new flux channels.">

*A coherent vortex mixes Fourier modes through unit wavevector shifts. Three layers of reachable sidebands restore the signed channel balance. The field illustrates the prescribed background; it is not a DNS snapshot. Channel values are certificate centers, in units of 10⁻⁶.*

## 1. The question: when does an isolated triad cease to predict transfer?

Waleffe’s instability assumption links isolated-triad stability to turbulent transfer [1]. More recent phase closures replace neighboring triads by weakly correlated noise, leading to a von Mises phase distribution under a Gaussian white-noise approximation [2, 3]. Strong coherent vortices are a revealing limit: the two-dimensional study explicitly identifies enhanced modal correlations as a source of closure failure [3].

**Card A isolates the missing feedback.** In a fixed-amplitude phase model derived from four Sabra shells, bidirectional phase feedback creates a strictly positive phase bias at a neutral self-interaction point where the isolated prediction is zero. In a neighboring open interval, the two predictions have opposite signs. Card B brings this question to a spatial PDE with evolving fluctuation amplitudes and a maintained cellular vortex.

## 2. A controlled PDE with an infinite-dimensional guarantee

On the periodic torus, decompose vorticity as

$$
\omega=A(\cos x+\cos y)+\epsilon\zeta,
\qquad \widehat\zeta_k=0\quad (|k|\le1).
$$

The background strength $A$ need not be small; $\epsilon$ controls fluctuation nonlinearity. With $G=(-\Delta)^{-1}$ and $J(f,g)=f_y g_x-f_x g_y$, measure the normalized, three-fluctuation-leg flux

$$
T_K(\zeta)=\langle GP_K\zeta,J(G\zeta,\zeta)\rangle,
\qquad \mathcal F_{K,N}(\epsilon)=\epsilon\mu_{\epsilon,N}(T_K).
$$

Here $P_K$ retains $1<|k|\le K$; positive flux is outward. The observable excludes the quadratic transfer containing a prescribed-background leg.

Viscous smoothing from $H^{-3/2}$ to $L^2$ has an integrable short-time singularity $t^{-3/4}$. Energy-moment and Poisson estimates then yield

$$
\big|\mathcal F_{K,N}(\epsilon)-\epsilon^2F_{A,K,N}\big|
\le C\epsilon^4,
\qquad F_{A,K,N}\longrightarrow F_{A,K},
$$

with $C$ independent of the Galerkin cutoff $N$, for fixed model parameters and trace-class noise. The numerical certificates below concern this leading coefficient; finite-$\epsilon$ accuracy also includes the remainder.

## 3. The certified shift, and what causes it

Fix $A=\nu=1$, $\alpha=0$, $K=2$. Force $\pm p,\pm q$, where $p=(3,0)$, $q=(-2,1)$ and the noise covariance weights are 9 and 5. The pair feeds the low mode $p+q=(1,1)$. Without the vortex, $F_{0,2}=-1/225$ exactly. With it,

$$
\begin{aligned}
F_{1,2}&\in[-0.003965854562651,-0.003965845004717],\\
\Delta F_1=F_{1,2}-F_{0,2}
&\in[0.000478589881793,0.000478599439728].
\end{aligned}
$$

Thus **$F_{1,2}<0$ and $\Delta F_1>0$**: reverse transfer is attenuated, without reversing direction. The certified attenuation is **10.768272%–10.768488%**, with absolute coefficient error radius **$<4.78\times10^{-9}$**. Complete infinite-lattice residuals account separately for solve, exterior/source-pruning and arithmetic errors.

B-M01 splits the third-moment response into connected and mean-product parts:

$$
F_A=t\kappa_{3,A}
+t\mathrm{Sym}(m_{1,A}\otimes U_A)
=F_A^{\rm conn}+F_A^{\rm mean}.
$$

$U_A$ is the Gaussian reference covariance; $\mathrm{Sym}$ is the sum of three placements. The mean term starts at $O(A^4)$, so the $A^2$ correction is entirely connected. At $A=1$:

| Contribution to $\Delta F_1$ | Approximate size, $10^{-6}$ | Certified share |
| :--- | ---: | ---: |
| Original connected-triad attenuation | +362.477 | 75.736047%–75.739564% |
| Other connected triads, net | +113.419 | 23.697093%–23.699571% |
| Induced mean response | +2.699 | 0.563853%–0.563872% |

The dominant change is a non-Gaussian, amplitude–phase response. It cannot be explained primarily by induced-mean advection.

## 4. Three sideband layers restore the signed balance

The background mixes $k$ with $k\pm e_x,k\pm e_y$ wherever the coupling coefficient is nonzero. Starting from the original triad and its conjugates, we retain successive **coupling-graph neighborhoods**, with unchanged forcing, coefficients and observable. No flux coefficients are fitted.

| Sideband depth | Signed modes | What the certificate reveals |
| :---: | ---: | :--- |
| 0 | 6 | Background projection vanishes; predicts $\Delta F=0$. |
| 1 | 20 | Original attenuation error $<0.71\%$; negative-channel error $>82.73\%$. |
| 2 | 38 | Negative-channel error $>5.1264\%$; fails the 5% target. |
| **3** | **62** | **All five targets pass; largest relative error $<0.08530\%$.** |

The new channels carry approximately **$+255.4\times10^{-6}$** and **$-142.4\times10^{-6}$**, leaving only $113.0\times10^{-6}$ in raw net transfer. Subtracting their mean contribution gives the connected net above. These are fixed B-M01 masks; unlisted channels retain an explicit error bound.

<img src="assets/convergence.png" width="900" alt="Certified upper bounds on five target errors: original attenuation converges early, while the negative channels require three sideband layers.">

*Each point is a certified relative-error upper bound against the infinite-model reference. All five targets must be below 5%. Separate lower bounds certify rejection of depths 0–2.*

**62 modes is minimal within this declared nested family**, not among every possible reduced model. The important physical distinction is that matching the original triad can look excellent while the signed sideband balance remains wrong.

## 5. Implications for LES and flow reconstruction

An energy spectrum constrains second-order amplitudes. Energy transfer additionally depends on amplitude-weighted, connected third-order phase organization. A coherent vortex acts as a multi-frequency mixer; a premature interaction cutoff can destroy the positive/negative compensation even when one dominant channel is accurate.

This motivates checking **connected response, both signed channels, and net flux together**. Internal triad phase is translation-invariant; paired spatial phase additionally tests whether a reconstructed vortex sits at its DNS position. These are different validation questions.

A bridge to 2D–3C slices is the common-filter diagnostic

$$
\Pi_\ell^\parallel=-\sum_{i=1}^{3}\sum_{\alpha=x,y}
\tau_{i\alpha}^{\ell}\,\partial_\alpha\bar u_i^{\ell},
\qquad \tau_{i\alpha}^{\ell}
=\overline{u_i u_\alpha}^{\ell}-\bar u_i^{\ell}\bar u_\alpha^{\ell},
$$

conditioned on coarse strain/vorticity backgrounds. This is the in-plane contribution, and the two-dimensional theorem supplies a mechanism to test, not a theorem for three-dimensional DNS or every SGS closure.

### References and evidence

1. F. Waleffe (1992), [The nature of triad interactions in homogeneous turbulence](https://ntrs.nasa.gov/citations/19920038608), *Physics of Fluids A* 4, 350–363. [DOI](https://doi.org/10.1063/1.858309).
2. S. J. Benavides & M. D. Bustamante (2026 version), [Phase dynamics and their role determining energy flux in hydrodynamic shell models](https://arxiv.org/html/2507.03397v2).
3. S. J. Benavides & M. D. Bustamante (2026 preprint), [Triad phase dynamics determine cascade direction in two-dimensional turbulence](https://arxiv.org/html/2605.03049v1).

[Proof outline and conventions](docs/mathematics.md) · [Exact certificates and lightweight checker](evidence/README.md) · [Figure sources](docs/figures.md)

*Analytic proofs with deterministic rational verification and one independent Challenger underpin the archived results. This discovery package presents those results and checks their exported arithmetic; it is not a proof-kernel formalization or a complete solver archive.*
