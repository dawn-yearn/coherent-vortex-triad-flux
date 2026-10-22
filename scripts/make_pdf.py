"""Compose the three-page discovery note from the frozen presentation."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.utils import ImageReader

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"discovery-note.pdf"
W,H=595.276,841.89
LEFT,RIGHT=43,43
WIDTH=W-LEFT-RIGHT
BLUE="#0072B2"; GRAY="#555555"; INK="#202020"
c=canvas.Canvas(str(OUT),pagesize=(W,H),pageCompression=1,invariant=1)
c.setTitle("How a coherent vortex reshapes triad energy transfer")
c.setSubject("Phase08: certified flux attenuation, connected response and a minimal sideband family")
y=0
page_number=0
def start(kicker):
    global y,page_number
    page_number+=1
    c.setFillColor(HexColor(BLUE));c.setFont("Helvetica-Bold",8.5)
    c.drawString(LEFT,H-32,"PHASE08  /  DISCOVERY NOTE")
    c.setFillColor(HexColor(GRAY));c.setFont("Helvetica",8)
    c.drawRightString(W-RIGHT,H-32,kicker)
    c.setStrokeColor(HexColor("#d9dfe3"));c.setLineWidth(.5)
    c.line(LEFT,47,W-RIGHT,47)
    c.setFont("Helvetica",8);c.setFillColor(HexColor(GRAY))
    c.drawString(LEFT,31,"Coherent vortices · Connected triads · Certified sidebands")
    c.drawRightString(W-RIGHT,31,f"{page_number:02d} / 03")
    y=H-60
def ensure():
    if y<58: raise RuntimeError(f"Page {page_number} overflow: {y}")
def paragraph(text,size=10.3,leading=13.6,after=7,color=INK,font="Times-Roman"):
    global y
    style=ParagraphStyle("p",fontName=font,fontSize=size,leading=leading,
                         textColor=HexColor(color),spaceAfter=0)
    obj=Paragraph(text,style);_,height=obj.wrap(WIDTH,900)
    y-=height;ensure();obj.drawOn(c,LEFT,y);y-=after
def title(text):
    paragraph(text,23,26,12,font="Helvetica-Bold")
def heading(text):
    global y
    y-=2
    paragraph(text,12.5,16,7,font="Helvetica-Bold")
def picture(name,width=WIDTH,after=5):
    global y
    image=ImageReader(str(ROOT/"assets"/name))
    iw,ih=image.getSize()
    if name.startswith("eq-"):
        width=min(width,iw/300*72*.82)
    height=width*ih/iw
    y-=height;ensure();c.drawImage(image,LEFT+(WIDTH-width)/2,y,width=width,height=height,mask="auto")
    y-=after
def table(rows,widths,size=9.3,after=9):
    global y
    ps=ParagraphStyle("cell",fontName="Times-Roman",fontSize=size,leading=size+3)
    contents=[[Paragraph(str(v),ps) for v in row] for row in rows]
    t=Table(contents,colWidths=widths,hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),HexColor("#eef3f6")),
        ("LINEBELOW",(0,0),(-1,0),.7,HexColor(BLUE)),
        ("LINEBELOW",(0,1),(-1,-1),.35,HexColor("#dce1e4")),
        ("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),7),("RIGHTPADDING",(0,0),(-1,-1),7),
        ("VALIGN",(0,0),(-1,-1),"TOP")
    ]))
    _,height=t.wrap(WIDTH,800)
    y-=height;ensure();t.drawOn(c,LEFT,y);y-=after
def finish():
    ensure();c.showPage()

start("The result & the model")
title("How a coherent vortex<br/>reshapes triad energy transfer")
paragraph("An order-one cellular vortex reorganizes connected three-point correlations. A controlled two-dimensional Navier-Stokes model quantifies the resulting flux shift with analytic proofs and exact-arithmetic bounds.",11,15,12)
stat_y=y
for i,(big,small) in enumerate([
    ("10.77%","attenuation of negative flux"),
    (">99.43%","of the shift is connected"),
    ("62 modes","three sideband layers")]):
    x=LEFT+i*(WIDTH/3)
    c.setFillColor(HexColor(BLUE));c.setFont("Helvetica-Bold",21)
    c.drawString(x,stat_y-21,big)
    c.setFillColor(HexColor(GRAY));c.setFont("Helvetica",8.1)
    c.drawString(x,stat_y-37,small)
y-=45
picture("mechanism.png")
paragraph("Analytic background (not DNS), certified sideband depths 0-3, and new signed-channel centers in units 10<super>-6</super>. Exact error bounds accompany the source data.",8.2,10.5,10,color=GRAY)

heading("1  /  Why isolated-triad intuition can fail")
paragraph("Waleffe links isolated-triad stability to turbulent transfer [1]. Recent phase closures replace neighboring triads with weakly correlated noise [2, 3]. Strong coherent vortices challenge this approximation by strengthening modal correlations [3].")
paragraph("<b>Card A isolates feedback.</b> In a fixed-amplitude four-shell Sabra phase model, coupled phases acquire a positive bias at a neutral point where the isolated prediction is zero; nearby, transfer signs disagree. Card B moves to a spatial PDE with evolving amplitudes.")

heading("2  /  A maintained cellular vortex plus fluctuations")
picture("eq-model.png",width=WIDTH-20,after=4)
paragraph("On the periodic torus, A need not be small; epsilon controls fluctuation nonlinearity. With G the inverse negative Laplacian, J(f,g) = f<sub>y</sub>g<sub>x</sub> - f<sub>x</sub>g<sub>y</sub>, and P<sub>K</sub> retaining 1 &lt; |k| &lt;= K, the normalized outward flux is",10.1,13.4,3)
picture("eq-observable.png",after=4)
paragraph("Only three fluctuation legs enter this observable. Viscous smoothing H<super>-3/2</super> to L<super>2</super> has integrable short-time singularity t<super>-3/4</super>. Together with uniform energy moments and Poisson reduction, it gives",10.1,13.4,3)
picture("eq-uniform.png",after=4)
paragraph("C is independent of the Galerkin cutoff N for fixed parameters. The certificates concern the leading coefficient F; finite-epsilon accuracy also includes the remainder.",9.2,12,0,color=GRAY)
finish()

start("The certified shift & its origin")
title("Where the 10.77% shift comes from")
paragraph("Set viscosity and background amplitude to one, with zero linear drag and cutoff K = 2. Force the four modes ±p, ±q with p = (3, 0), q = (-2, 1), and covariance weights 9 and 5. Their interaction feeds the low mode p + q = (1, 1). With no background, F<sub>0,2</sub> = -1/225 exactly.",10.5,14.1,10)
table([
    ["<b>Infinite-model coefficient</b>","<b>Certified outward enclosure</b>"],
    ["F<sub>1,2</sub>","[-0.003965854562651, -0.003965845004717]"],
    ["Delta F<sub>1</sub> = F<sub>1,2</sub> + 1/225","[0.000478589881793, 0.000478599439728]"],
],[155,WIDTH-155],9.4)
paragraph("<b>F remains negative; its change is strictly positive.</b> The negative-flux amplitude decreases by 10.768272%-10.768488%. This is attenuation, without a direction reversal. The absolute coefficient error radius is below <b>4.78 × 10<super>-9</super></b>.")

heading("3  /  Connected response supplies almost all of the change")
picture("eq-decomposition.png",after=5)
paragraph("U<sub>A</sub> is the Gaussian reference covariance; m<sub>1,A</sub> is the first nonlinear mean response. Sym is the sum of three placements. The connected term removes the part of the third moment explained by mean times covariance. It retains amplitude-phase organization that cannot be reduced to a mean-flow artifact.")
paragraph("<b>The mean contribution begins at order A<super>4</super>.</b> The leading A<super>2</super> correction is therefore entirely connected. At A = 1, the certified decomposition is:")
table([
    ["<b>Contribution to the shift</b>","<b>Center × 10<super>6</super></b>","<b>Certified share (%)</b>"],
    ["Original connected-triad attenuation","+362.477","75.736047-75.739564"],
    ["Other connected triads, net","+113.419","23.697093-23.699571"],
    ["Induced mean response","+2.699","0.563853-0.563872"],
],[220,92,WIDTH-312],9.2)
paragraph("The original triad supplies about 75.7% of the shift. The other channels supply about 23.7% net, but their raw positive and negative groups are much larger: <b>+255.4</b> and <b>-142.4</b>, in units 10<super>-6</super>. Their compensation leaves 113.0; removing the complement's mean term gives the connected net 113.4.")
paragraph("These groups use the fixed B-M01 sign masks. The unlisted complement remains enclosed by an explicit error bound; the construction does not classify every unknown infinite-tail orbit.",9.4,12.5,7,color=GRAY)

heading("How the numerical claim becomes a certificate")
paragraph("Sparse rational moment candidates are tested on the entire infinite lattice, including every generated exterior output. A sharp dual norm of 1/720 converts residual bounds into scalar flux error. Independent code checks the same result; floating-point convergence alone is not the certificate.",10.2,13.5,7)
table([
    ["<b>Error budget</b>","<b>Approximate rigorous bound</b>"],
    ["Finite solve","6.031742283070 × 10<super>-10</super>"],
    ["Exterior + source pruning","4.175792455590 × 10<super>-9</super>"],
    ["Directed arithmetic","1.538205296343 × 10<super>-24</super>"],
],[WIDTH*.55,WIDTH*.45],9.2,after=5)
paragraph("Acceptance uses saved exact fractions. The total radius is 4.778966683897 × 10<super>-9</super>. The exported checker reconciles those fractions; it does not rerun the full nonlinear residual construction.",9.2,12,0,color=GRAY)
finish()

start("The minimal family & the LES implication")
title("Three layers restore the signed balance")
paragraph("The cellular vortex shifts wavevectors by ±e<sub>x</sub> and ±e<sub>y</sub> wherever the coupling is nonzero. Starting from the original triad and its conjugates, B-R01 adds successive coupling-graph neighborhoods. Forcing, equation coefficients and observable stay fixed; no flux coefficients are fitted.")
picture("convergence.png",after=4)
paragraph("Points are certified relative-error upper bounds against the infinite-model reference. All five targets must meet the 5% rule. Separate lower bounds prove failure of depths 0-2.",8.2,10.5,9,color=GRAY)
paragraph("The 6-mode model predicts no shift. At 20 modes, original attenuation is within 0.71%, yet negative-channel error exceeds 82.73%. At 38 modes, it still exceeds 5.1264%. Only 62 modes pass all five targets, each below 0.08530%.",10.2,13.5,9)
paragraph("<b>62 modes is minimal within this declared family, not over all reductions.</b> Matching the original triad alone can hide a badly distorted signed balance.",10.2,13.5,9)

heading("4  /  What this suggests for LES and reconstruction")
paragraph("Matching E(k) constrains amplitudes, while transfer also depends on connected, amplitude-weighted phase organization. A coherent vortex mixes frequencies: early truncation breaks signed compensation. Check connected response, both signed channels and net flux together.")
paragraph("Internal triad phase is translation-invariant; spatial pairing additionally tests vortex position. A 2D-3C diagnostic bridge uses common in-plane filtering, conditioned on coarse strain/vorticity:")
picture("eq-diagnostic.png",after=5)
paragraph("This is only the in-plane contribution. The controlled 2D theorem supplies a mechanism to test in DNS; it is not a universal claim about three-dimensional cascades or all SGS closures.",9.2,12,8,color=GRAY)

heading("References & evidence")
paragraph('[1] F. Waleffe (1992). <a href="https://doi.org/10.1063/1.858309" color="#0072B2">The nature of triad interactions in homogeneous turbulence.</a><br/>'
          '[2] S. J. Benavides &amp; M. D. Bustamante (2026 version). <a href="https://arxiv.org/html/2507.03397v2" color="#0072B2">Phase dynamics and their role determining energy flux in hydrodynamic shell models.</a><br/>'
          '[3] S. J. Benavides &amp; M. D. Bustamante (2026 preprint). <a href="https://arxiv.org/html/2605.03049v1" color="#0072B2">Triad phase dynamics determine cascade direction in two-dimensional turbulence.</a>',
          8.4,11.1,5)
paragraph("Companion repository: bilingual text, mathematical contract, exact certificates, source hashes and reproducible figures. Underlying research: one Lead, one independent Challenger, 60-second numerical command limit.",8.6,11.4,0,color=GRAY)
finish()
c.save()
print("Created discovery-note.pdf: 3 composed pages")
