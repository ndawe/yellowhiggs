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
            mass, xs_mean, \
            error_high_full, error_low_full, \
            error_high_scale, error_low_scale, \
            error_high_pdf, error_low_pdf = map(abs, map(float, line))
        except ValueError, e:
            raise ValueError("line not understood: %s\n%s" % (line, e))

        info = {}
        error = {}
        error_full = {}
        error_scale = {}
        error_pdf = {}
        error['full'] = error_full
        error['scale'] = error_scale
        error['pdf'] = error_pdf
        info['VALUE'] = xs_mean
        info['ERROR'] = error
        xs[mass] = info

        error_high_full_factor = 1 + error_high_full / 100.
        error_low_full_factor = 1 - error_low_full / 100.

        error_full['value'] = (xs_mean * error_high_full_factor,
                               xs_mean * error_low_full_factor)
        error_full['percent'] = (error_high_full,
                                 error_low_full)
        error_full['factor'] = (error_high_full_factor,
                                error_low_full_factor)

        error_high_scale_factor = 1 + error_high_scale / 100.
        error_low_scale_factor = 1 - error_low_scale / 100.

        error_scale['value'] = (xs_mean * error_high_scale_factor,
                                xs_mean * error_low_scale_factor)
        error_scale['percent'] = (error_high_scale,
                                  error_low_scale)
        error_scale['factor'] = (error_high_scale_factor,
                                 error_low_scale_factor)

        error_high_pdf_factor = 1 + error_high_pdf / 100.
        error_low_pdf_factor = 1 - error_low_pdf / 100.

        error_pdf['value'] = (xs_mean * error_high_pdf_factor,
                              xs_mean * error_low_pdf_factor)
        error_pdf['percent'] = (error_high_pdf,
                                error_low_pdf)
        error_pdf['factor'] = (error_high_pdf_factor,
                               error_low_pdf_factor)
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


def xs(energy, mass, mode,
       error='full',
       error_type='value'):
    """
    Return the production cross section [pb] in this mode in the form:
    (xs, xs_high, xs_low)
    """
    mode = mode.lower()
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

    info = __XS[energy][mode][mass]
    return info['VALUE'], info['ERROR'][error][error_type]


def br(mass, channel):
    """
    Return the branching ratio for this channel
    """
    channel = channel.lower()
    if channel not in __BR:
        raise ValueError("channel '%s' not understood. Use one of %s" %
                         (channel, ', '.join(__BR.keys())))
    if mass not in __BR[channel]:
        raise ValueError("mass point %.1f [GeV] not recorded for channel '%s'" %
                         (mass, channel))
    return __BR[channel][mass]


def xsbr(energy, mass, mode, channel,
         error='full',
         error_type='value'):
    """
    Return the production cross section [pb] times branching ratio for this mode and
    channel in the form:
    (xsbr, xsbr_high, xsbr_low)
    """
    _xs, (xs_high, xs_low) = xs(energy, mass, mode,
                                error=error,
                                error_type=error_type)
    _br = br(mass, channel)
    if error_type == 'value':
        return _xs * _br, (xs_high * _br, xs_low * _br)
    else:
        return _xs * _br, (xs_high, xs_low)
