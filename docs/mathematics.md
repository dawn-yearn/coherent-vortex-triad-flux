# Mathematical scope and certificate contract

[Discovery note](../README.md) · [Exact data](../evidence/README.md)

This appendix records the conventions, proof structure and error contracts behind the discovery note. It is a condensed account of the Phase08 analytic arguments; the exported checker validates certificate arithmetic and does not replace the analytic proofs.

## Card A: feedback can select the opposite sign

With standard Sabra coefficients $a=1$, $b=c=-1/2$, wavenumbers $2^n$ and fixed amplitudes $(r,1,2,1/2)$, the two phases satisfy

$$
\begin{aligned}
d\theta&=\big[(5r/2-4/r)\cos\theta-(9/2)\cos\psi\big]dt+\sqrt{2D}\,dW_1,\\
d\psi&=\big[(9/2)\cos\psi+(3r/2)\cos\theta\big]dt+\sqrt{2D}\,dW_2.
\end{aligned}
$$

At $r_*=\sqrt{8/5}$ the isolated self-interaction vanishes. The invariant-density entropy identity expresses $\mathbb E\sin\theta$ as a positive multiple of Fisher information. The density cannot be uniform, so this bias is strictly positive for every $D>0$. The isolated process has zero bias there. Continuity gives an adjacent open interval with negative isolated bias and positive coupled bias. The associated target-triad energy transfers are $(-4r,2r,2r)\sin\theta$.

An autonomous additive bath with no response to the target phase leaves that phase uniform at the neutral point. This identifies a missing feedback mechanism in this specified fixed-amplitude closure; it is not a statement about the full amplitude-evolving Sabra dynamics.

## Card B: model and uniform expansion

Let $\psi=\cos x+\cos y$, $G=(-\Delta)^{-1}$, $J(f,g)=f_y g_x-f_x g_y$ and $P$ exclude $|k|\le1$. The maintained-background fluctuation equation is

$$
d\zeta=\left[\nu\Delta\zeta-\alpha\zeta
-A P J\big(\psi,(I-G)\zeta\big)
-\epsilon P J(G\zeta,\zeta)\right]dt+\sqrt{2Q}\,dW.
$$

The torus inner product is spatially normalized. Real fields obey $\widehat\zeta_{-k}=\overline{\widehat\zeta_k}$. At the certified point, $A=\nu=1$, $\alpha=0$, $K=2$, and $Q_{\pm(3,0)}=9$, $Q_{\pm(-2,1)}=5$, with all other forcing weights zero.

The analytic argument uses the coercive energy structure on $|k|>1$, uniform invariant moments, the quadratic estimate into $H^{-3/2}$, and viscous smoothing with an integrable $t^{-3/4}$ singularity. Cubic Poisson reduction and symmetry give

$$
\mathcal F_{K,N}(\epsilon)=\epsilon^2F_{A,K,N}+O(\epsilon^4),
\qquad F_{A,K,N}\to F_{A,K},
$$

uniformly in $N$ for fixed parameters. The small parameter is fluctuation nonlinearity, not the background amplitude. This normalized flux is $\epsilon\mu(T_K)$; the dimensional three-fluctuation contribution for $\omega=A\psi+\epsilon\zeta$ carries the corresponding additional amplitude scaling.

## B-Q01 and B-S01: from a tail theorem to an infinite residual

The global bound at the fixed point is

$$
|F_{1,2}-F_{1,2,N}|\le\frac{13538259}{2}\left(\frac23\right)^N,
\qquad N\ge3.
$$

The sharper sign certificate uses a finitely supported rational candidate directly on the **infinite lattice**. It counts every generated exterior output and bounds all pruned covariance products; adding the global tail again would double count uncertainty.

For $D_j=\sum_{a=1}^j|k_a|^2$, $B_j=C_jD_j^{-1}$, the established bound $\|B_j\|_{1\to1}\le1/2$ gives a resolvent norm at most 2. Permutations and simultaneous wavevector reversal permit storage of orbit masses. The sharp scalar dual norm is

$$
\|tD_3^{-1}\|_{\infty,\mathrm{sym}}=\frac1{720}.
$$

It is attained by the original triad. An exact enumeration of 1,288 core triads is completed by an analytic exterior estimate; the adjoint functional still includes high-high pairs summing to a low mode.

If $\eta_j$ are full residual bounds for transformed moment candidates, $a=\|D_2\widehat U\|_1$, and $\overline U\le\min(112,a+2\eta_2)$ bounds the true transformed covariance norm, then

$$
|F-\widehat F|
\le \frac{\eta_3}{360}+\frac7{15}\eta_1
+\left(\frac7{30}+\frac{\overline U+a}{160}\right)\eta_2.
$$

The [selected exact certificate](../evidence/full_certificate.json) gives:

| Error source | Approximate rigorous bound |
| :--- | ---: |
| Finite solve | $6.031742283070\times10^{-10}$ |
| Spatial exterior | $1.432538283575\times10^{-12}$ |
| Pruned source products | $4.174359917306\times10^{-9}$ |
| Directed arithmetic | $1.538205296343\times10^{-24}$ |
| Total radius | $4.778966683897\times10^{-9}$ |

Acceptance uses rational fractions, not these display decimals. The exact shift by $1/225$ adds no error. The independently generated [Challenger certificate](../evidence/full_independent.json) agrees on the candidate center and certifies the same signs, with a negligible difference in arithmetic-error accounting.

The covariance, mean and cubic candidates contain 8,032, 136 and 114,079 orbits, respectively. No dense cubic tensor is needed. The label “N=12” describes covariance construction and residual bookkeeping, not an unaccounted radial cubic truncation.

## B-M01: connected response and signed masks

Writing $S(m,U)_{ijk}=m_iU_{jk}+m_jU_{ik}+m_kU_{ij}$, the moment equations imply

$$
(D_3-C_3)S(m_1,U)=S(N_1U,U)+Hm_1,
$$

$$
(D_3-C_3)\kappa_3=N_3W(U)-S(N_1U,U).
$$

The disconnected source cancels in the connected equation. The flux still contains the separately evaluated mean product. At $A=0$, $m_1=0$ and $F_0^{\rm mean}=0$. Exact finite-path coefficients give

$$
F_A^{\rm mean}
=\frac{33723207943065097}{10061841294293069531250}A^4+O(A^6),
$$

$$
F_A=F_0+
\frac{1189266237979024679}{2226224929818298500000}A^2+O(A^4).
$$

Thus the leading $A^2$ correction is wholly connected. This cumulant response combines amplitudes and phases; it is not an unweighted phase-correlation statistic.

At $A=1$, the original orbit is all permutations and simultaneous reversal of $((3,0),(-2,1),(-1,-1))$. The remaining fixed positive and negative masks contain 74 and 97 candidate orbits. Their aggregate signs are certified; the signs of every unknown tail orbit are not classified. The unlisted raw complement has radius below $4.779\times10^{-9}$. Exact row/column identities hold at candidate level; correlated component errors must not be mistaken for independent uncertainties.

## B-R01: the precise meaning of “minimal”

Start from $S_0=\{\pm p,\pm q,\pm(p+q)\}$. At each depth, adjoin all nonzero background-coupled neighbors:

$$
S_{d+1}=S_d\cup
\{l+e:\ l\in S_d,\ e\in\{\pm e_x,\pm e_y\},
\ |l+e|>1,\ e\times l\ne0\}.
$$

At $A=1$,

$$
C_{l+e,l}=-\frac{(e\times l)(|l|^2-1)}{2|l|^2}.
$$

The counts are $6,20,38,62$. The six-mode set has $P_{S_0}CP_{S_0}=0$, hence predicts no background shift. All projected models keep the original nonlinear interactions, noise and coefficients; none is fitted.

For full/reduced candidate centers $f,s$ and rigorous radii $r_f,r_s$, the reported relative-discrepancy enclosure is

$$
\frac{\max(0,|s-f|-r_s-r_f)}{|f|+r_f}
\le\frac{|F_S-F|}{|F|}
\le\frac{|s-f|+r_s+r_f}{|f|-r_f}.
$$

The full reference interval excludes zero for all five targets. Depth 2 has a negative-channel **lower** error bound above 5.1264%; depth 3 has all five **upper** bounds below 0.08530%. Minimality is therefore certified within this nested family and this 5% acceptance rule.

The 62-mode finite solve radius is below $9.44\times10^{-15}$, with exact rational evaluation and an unpruned source. Model deletion error is assessed against the full infinite-model certificate; the tiny finite solve radius alone is not a truncation-error bound.

The historical workflow used one Lead, one independent Challenger, deterministic checks and at most 60 seconds per numerical command. This publication export performs only arithmetic reconciliation, analytic illustration and document rendering.
