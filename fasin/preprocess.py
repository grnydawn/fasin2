# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os, re
from .util import fixedform_extensions, CMAPSTR, SMAPSTR

match_include = re.compile(r'^\s*include\s+(?P<quote>[\'"])(?P<path>[^\r\n]+\r?\n)$', re.I)

def _read_include(path, isstrict):
    lines = []
    for line in  open(path, 'r').readlines():
        match = match_include.match(line)
        if match is not None:
            quote = match.group('quote')
            path = match.group('path')
            pos = path.find(quote)
            lines.append(_read_include(path[:pos], isstrict))
        else:
            lines.append(line)
    return ''.join(lines)

def _fixed2freeform(text, isstrict):
    buf = []
    lines = text.split("\n")
    N = len(lines)
    for line0, line1 in zip(lines[:N-1], lines[1:N]):
        L0 = len(line0)
        L1 = len(line1)
        processed = False
        for idx, ch in enumerate(line0[:min(6,L0)]):
            if idx==0:
                if line0[0] in ["!", "C", "*"]:
                    buf.append("!"+line0[1:])
                    processed = True
                    break
            elif idx>0 and idx<5:
                if line0[idx] == "!":
                    buf.append(line0)
                    processed = True
                    break
        if not processed:
            tmp = []
            if L0>5:
                if line0[5] not in [" ", "0"]:
                    tmp.append("&")
                tmp.append(line0[6:])
            if L1>5:
                if line1[5] not in [" ", "0"]:
                    tmp.append("&")
            if tmp:
                buf.append(''.join(tmp))
    return "\n".join(buf)+"\n"

def _freeform_continuation(text, isstrict):
    buf = []
    A = []
    amark0 = None
    amark1 = None
    for idx, ch in enumerate(text):
        if amark0:
            if ch == "\n":
                amark0 = None
                amark1 = idx + 1
        elif amark1:
            if ch == "&":
                if ''.join(A).strip() == "":
                    amark1 = None
                else:
                    buf.extend(A)
                    amark0 = idx
                    amark1 = None
                A = []
            elif ch == "\n":
                if not ''.join(A).strip().startswith("@C"):
                    buf.extend(A)
                    amark0 = None
                    amark1 = None
                A = []
            elif ch == ";":
                A.append("\n")
            else:
                A.append(ch)
        elif ch == "&":
            amark0 = idx
        elif ch == ";":
            buf.append("\n")
        else:
            buf.append(ch)
    return ''.join(buf)

def _freeform_string_comment(text, isstrict):
    smap = {}
    cmap = {}
    buf = []
    S = []
    skip = False
    quote = None
    cmark = None
    L = len(text)
    for idx, ch in enumerate(text):
        if skip:
            skip = False
            continue

        if quote:
            if ch == quote[0]:
                if idx+1 < L and text[idx+1] == ch:
                    S.append(ch)
                    skip = True
                else:
                    tmp = []
                    cont = False
                    for s in S:
                        if s=="&":
                            cont = not cont
                        elif not cont:
                            tmp.append(s)
                    assert not cont, "Wrong literal string syntax."
                    sidx = len(smap)
                    smap[sidx] = ''.join(tmp)
                    buf.append(SMAPSTR%sidx)
                    S = []
                    quote = None
            else:
                S.append(ch)
        elif ch in ["'", '"']:
            quote = (ch, idx)
        elif ch == "!":
            cmark = idx
        elif ch in ["\r", "\n"]:
            if cmark:
                cidx = len(cmap)
                cmap[cidx] = text[cmark:idx]
                buf.append(CMAPSTR%cidx)
                buf.append(ch)
                cmark = None
            else:
                buf.append(ch)
        else:
            if cmark is None:
                buf.append(ch)
    return ''.join(buf), smap, cmap

def transform(path, isfree=None, isstrict=False):
    _, ext = os.path.splitext(path)
    if isfree is None and isstrict is not True:
        isfree = not ext in fixedform_extensions
    source = _read_include(path, isstrict)
    if isfree is False:
        source = _fixed2freeform(source, isstrict)
    if isfree is None and isstrict is True:
        raise Exception('Please specify Fortran source form.')
    source, strmap, cmtmap = _freeform_string_comment(source, isstrict)
    source = _freeform_continuation(source, isstrict)
    #import pdb; pdb.set_trace()
    print(source, strmap, cmtmap)
    return source, strmap, cmtmap

