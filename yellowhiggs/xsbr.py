"""
This module handles retrieving the official Higgs cross sections [pb] and
branching ratios. See dat/README
"""
import os
from glob import glob
from pkg_resources import resource_stream, resource_listdir
from math import sqrt

__all__ = [
    'xs',
    'br',
    'xsbr',
]


def _read_xs_file(filename):
    xs = {}
    f = resource_stream('yellowhiggs', filename)
    for line in f.readlines():
        line = line.strip()
        if line.startswith('#'):
            # skip the header line
            continue
        line = line.split()
        try:
            mass, xs_mean, \
            error_high_scale, error_low_scale, \
            error_high_pdf, error_low_pdf = map(abs, map(float, line[:6]))
        except ValueError, e:
            raise ValueError("line not understood: %s\n%s" % (line, e))

        # linear combination of errors
        error_high_full = error_high_scale + error_high_pdf
        error_low_full = error_low_scale + error_low_pdf

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
    header = {}
    for i, line in enumerate(f.readlines()):
        line = line.strip().split()
        if i == 0:
            # First line contains channel labels
            # Ignore first column which is the Higgs mass
            channels = line[1:]
            for j, channel in enumerate(channels):
                header[channel] = j + 1
                if channel[:1] in ['+', '-']:
                    continue
                br[channel] = {}
        else:
            try:
                line = map(float, line)
            except ValueError, e:
                raise ValueError("line not understood: %s\n%s" % (line, e))
            for channel, value in zip(channels, line[1:]):
                if channel[:1] in ['+', '-']:
                    continue
                error_high = 0.
                error_low = 0.
                if '+' + channel in header:
                    error_high = abs(line[header['+' + channel]])
                if '-' + channel in header:
                    error_low = abs(line[header['-' + channel]])
                error_high_factor = 1. + error_high / 100.
                error_low_factor = 1. - error_low / 100.
                error = {}
                error['value'] = (
                    value * error_high_factor, value * error_low_factor)
                error['percent'] = (
                    error_high, error_low)
                error['factor'] = (
                    error_high_factor, error_low_factor)
                info = {}
                info['ERROR'] = error
                info['VALUE'] = value
                br[channel][line[0]] = info
    f.close()
    return br


MODES = {}
energy_dirs = resource_listdir('yellowhiggs', os.path.join('dat', 'xs'))
ENERGIES = map(float, energy_dirs)

__XS = {}
for energy, energy_dir in zip(ENERGIES, energy_dirs):
    mode_files = resource_listdir(
        'yellowhiggs', os.path.join('dat', 'xs', energy_dir))
    modes = [mode.split('.')[0] for mode in mode_files]
    MODES[energy] = modes
    __XS[energy] = {}
    for mode, mode_file in zip(modes, mode_files):
        __XS[energy][mode] = _read_xs_file(
            os.path.join('dat', 'xs', energy_dir, mode_file))

__BR = {}
for channel_file in resource_listdir(
        'yellowhiggs', os.path.join('dat', 'br')):
    __BR.update(_read_br_file(os.path.join('dat', 'br', channel_file)))


def adderrors(errors, error_type, value=0.):
    """
    Sum percent errors in quadrature and return (high, low), either as
    error_type = 'value', 'percent' or 'factor'
    """
    total_high, total_low = 0., 0.
    for high, low in errors:
        total_high += (high / 100.)**2.
        total_low += (low / 100.)**2.
    total_high = sqrt(total_high)
    total_low = sqrt(total_low)
    if error_type == 'value':
        return (1. + total_high) * value, (1. - total_low) * value
    elif error_type == 'percent':
        return total_high * 100., total_low * 100.
    else:
        return (1. + total_high), (1. - total_low)


def xs(energy, mass, mode,
       error='full',
       error_type='value'):
    """
    xs(energy, mass, mode, error='full', error_type='value')
    Return the production cross section [pb] in this mode in the form:
    (xs, (xs_high, xs_low))
    """
    mode = mode.lower()
    if energy not in __XS:
        raise ValueError(
            "no cross sections recorded for energy %.1f TeV. "
            "Use one of %s" %
                (energy, ', '.join(map(str, __XS.keys()))))
    if mode not in __XS[energy]:
        raise ValueError(
            "production mode '%s' not understood. Use one of %s" %
                (mode, ', '.join(__XS[energy].keys())))
    if mass not in __XS[energy][mode]:
        raise ValueError(
            "mass point %.1f GeV not recorded for production mode '%s'" %
                (mass, mode))
    info = __XS[energy][mode][mass]
    return info['VALUE'], info['ERROR'][error][error_type]


def br(mass, channel,
       error_type='value'):
    """
    br(mass, channel, version='v2', error_type=None): --> float
    Return the branching ratio for this channel

    error_type = 'value', 'percent' or 'factor'
    """
    if channel not in __BR:
        raise ValueError(
            "channel '%s' not understood. Use one of %s" %
                (channel, ', '.join(__BR.keys())))
    if mass not in __BR[channel]:
        raise ValueError(
            "mass point %.1f [GeV] not recorded for channel '%s'" %
                (mass, channel))
    info = __BR[channel][mass]
    return info['VALUE'], info['ERROR'][error_type]


def xsbr(energy, mass, mode, channel,
         error='full',
         error_type='value'):
    """
    Return the production cross section [pb] times branching ratio for this mode and
    channel in the form:
    (xsbr, xsbr_high, xsbr_low)
    """
    _xs, xs_error = xs(energy, mass, mode, error=error, error_type='percent')
    _br, br_error = br(mass, channel, error_type='percent')
    value = _xs * _br
    error_high, error_low = adderrors(
        [xs_error, br_error], error_type, value=value)
    return value, (error_high, error_low)
