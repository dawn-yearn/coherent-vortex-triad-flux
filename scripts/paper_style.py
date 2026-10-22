"""Shared style for new research figures; historical renderers remain frozen."""
from contextlib import contextmanager

import matplotlib as mpl
from cycler import cycler

DNS_COLOR = '#202020'
COLORS = ('#0072B2', '#009E73', '#D55E00', '#CC9900', '#CC79A7', '#56B4E9')
LINESTYLES = ('-', '--', '-.', ':', (0, (6, 2)), (0, (3, 1, 1, 1)))
SIGNED_CMAP = 'RdBu_r'
SEQUENTIAL_CMAP = 'Blues'


def style_parameters(font_size=13):
    """No global rcParams mutation; callers may use this dict with rc_context."""
    return {
        'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'],
        'mathtext.fontset': 'stix', 'font.size': font_size,
        'axes.labelsize': font_size + 2, 'axes.titlesize': font_size,
        'xtick.labelsize': font_size - 1, 'ytick.labelsize': font_size - 1,
        'axes.linewidth': .9, 'axes.edgecolor': DNS_COLOR, 'axes.labelcolor': DNS_COLOR,
        'text.color': DNS_COLOR, 'xtick.color': DNS_COLOR, 'ytick.color': DNS_COLOR,
        'axes.spines.top': True, 'axes.spines.right': True,
        'xtick.direction': 'in', 'ytick.direction': 'in', 'xtick.top': True, 'ytick.right': True,
        'xtick.major.size': 5, 'ytick.major.size': 5,
        'xtick.minor.size': 2.5, 'ytick.minor.size': 2.5,
        'axes.grid': False, 'legend.frameon': False, 'legend.fontsize': font_size - 3,
        'axes.prop_cycle': cycler(color=COLORS), 'lines.linewidth': 1.4,
        'figure.facecolor': 'white', 'axes.facecolor': 'white', 'savefig.facecolor': 'white',
        'pdf.fonttype': 42, 'ps.fonttype': 42, 'savefig.dpi': 300,
    }


@contextmanager
def paper_style(font_size=13, **overrides):
    """Context for statistics, error curves and fields; restores caller settings."""
    with mpl.rc_context({**style_parameters(font_size), **overrides}):
        yield


def curve_style(index=0, *, reference=False, color=None, linestyle=None):
    """Stable defaults; explicit method colors/styles should be reused across figures."""
    ls = linestyle if linestyle is not None else ('-' if reference else LINESTYLES[index % len(LINESTYLES)])
    if isinstance(ls, list):
        ls = (ls[0], tuple(ls[1]))
    return dict(color=color or (DNS_COLOR if reference else COLORS[index % len(COLORS)]),
                linestyle=ls, linewidth=1.65 if reference else 1.4, zorder=5 if reference else 3)
