import os
import traceback
from io import StringIO
from subprocess import PIPE, Popen, TimeoutExpired


def popen(cmd, sys_env=True, **kwargs):
    if isinstance(cmd, list):
        for i in range(len(cmd)):
            if not isinstance(cmd[i], str):
                cmd[i] = str(cmd[i])

    kwargs.setdefault('encoding', 'utf-8')
    kwargs.setdefault('stdin', PIPE)
    kwargs.setdefault('stdout', PIPE)
    kwargs.setdefault('stderr', PIPE)

    if sys_env and kwargs.get('env') is not None:
        kwargs['env'] = os.environ.copy().update(kwargs['env'])
    return Popen(cmd, **kwargs)


def execute(cmd, input_str=None, timeout=None, **kwargs):
    p = popen(cmd, **kwargs)
    try:
        out, err = p.communicate(input_str, timeout=timeout)
    except TimeoutExpired:
        out = ''
        err = get_exception()
        p.kill()
    stat = p.returncode

    if isinstance(out, str):
        out = out.rstrip('\n')
    return stat, out, err


def execute_get_out(cmd, **kwargs):
    [_, out, _] = execute(cmd, **kwargs)
    return out


def get_exception():
    with StringIO() as io:
        traceback.print_exc(file=io)
        io.seek(0)
        content = io.read()

    return content


def reg_find_one(reg, content, default=''):
    res = reg.findall(content)
    if len(res) > 0:
        return res[0]
    else:
        return default


def compare_version(a: str, b: str, ex=False):
    sa = a.split('-')
    sb = b.split('-')

    if ex is False and len(sb) > 1:
        return False
    else:
        return int(sa[0].replace('.', '')) < int(sb[0].replace('.', ''))


def zfill_bytes(data, size):
    fill_size = size - len(data)
    if fill_size > 0:
        data += b'\x00' * fill_size
    return data
