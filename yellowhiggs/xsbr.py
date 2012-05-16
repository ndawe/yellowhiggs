"""
This module handles retrieving the official Higgs cross sections [pb] and
branching ratios. See dat/README
"""
import os
from glob import glob
from pkg_resources import resource_stream, resource_listdir


__all__ = [
    'xs',
    'br',
    'xsbr',
]

__HERE = os.path.dirname(os.path.abspath(__file__))


def _read_xs_file(filename):

    xs = {}
    f = resource_stream('yellowhiggs', filename)
    for line in f.readlines():
        line = line.strip()
        if line.startswith('#'):
            continue
        line = line.split()
        try:
            mass, xs_mean, error_high, error_low = map(float, line[:4])
        except ValueError, e:
            raise ValueError("line not understood: %s\n%s" % (line, e))

        xs[mass] = (xs_mean,
                    xs_mean * (1. + abs(error_high) / 100.),
                    xs_mean * (1. - abs(error_low) / 100.))
    f.close()
    return xs


def _read_br_file(filename):

    br = {}
    f = resource_stream('yellowhiggs', filename)
    for i, line in enumerate(f.readlines()):
        line = line.strip().split()
        if i == 0:
            # First line contains channel labels
            # Ignore first column which is the Higgs mass
            channels = line[1:]
            for channel in channels:
                br[channel] = {}
        else:
            try:
                line = map(float, line)
            except ValueError, e:
                raise ValueError("line not understood: %s\n%s" % (line, e))
            for channel, value in zip(channels, line[1:]):
                br[channel][line[0]] = value
    f.close()
    return br


MODES = {}
energy_dirs = resource_listdir('yellowhiggs', os.path.join('dat', 'xs'))
ENERGIES = map(float, energy_dirs)

__XS = {}
for energy, energy_dir in zip(ENERGIES, energy_dirs):
    mode_files = resource_listdir('yellowhiggs', os.path.join('dat', 'xs', energy_dir))
    modes = [mode.split('.')[0] for mode in mode_files]
    MODES[energy] = modes
    __XS[energy] = {}
    for mode, mode_file in zip(modes, mode_files):
        __XS[energy][mode] = _read_xs_file(os.path.join('dat', 'xs', energy_dir, mode_file))

__BR = {}
for channel_file in resource_listdir('yellowhiggs', os.path.join('dat', 'br')):
    __BR.update(_read_br_file(os.path.join('dat', 'br', channel_file)))


def xs(energy, mass, mode):
    """
    Return the production cross section [pb] in this mode in the form:
    (xs, xs_high, xs_low)
    """
    if energy not in __XS:
        raise ValueError(("no cross sections recorded for energy %.1f TeV. "
                          "Use one of %s") %
                          (energy, ', '.join(map(str, __XS.keys()))))
    if mode not in __XS[energy]:
        raise ValueError("production mode '%s' not understood. Use one of %s" %
                         (mode, ', '.join(__XS[energy].keys())))
    if mass not in __XS[energy][mode]:
        raise ValueError("mass point %.1f GeV not recorded for production mode '%s'" %
                         (mass, mode))

    return __XS[energy][mode][mass]


def br(mass, channel):
    """
    Return the branching ratio for this channel
    """
    if channel not in __BR:
        raise ValueError("channel '%s' not understood. Use one of %s" %
                         (channel, ', '.join(__BR.keys())))
    if mass not in __BR[channel]:
        raise ValueError("mass point %.1f [GeV] not recorded for channel '%s'" %
                         (mass, channel))
    return __BR[channel][mass]


def xsbr(energy, mass, mode, channel):
    """
    Return the production cross section [pb] times branching ratio for this mode and
    channel in the form:
    (xsbr, xsbr_high, xsbr_low)
    """
    _xs, xs_high, xs_low = xs(energy, mass, mode)
    _br = br(mass, channel)
    return (_xs * _br, xs_high * _br, xs_low * _br)
