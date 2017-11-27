# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os, re
from .util import fixedform_extensions, CMAPSTR, SMAPSTR
from parglare import Parser, GLRParser, Grammar

f2003_grammar = r"""
    // Fortran2003 grammar specification excerpt from J3/04-007
    // __version__ : 0.1.0

    ///////////////// Fortran high-level concepts /////////////////
    program                 : program_unit+;
    program_unit            : main_program | CBL;
    main_program            : end_program_stmt;


    ///////////////// end statements ///////////////////////////////
    end_program_stmt        : LBL? END program_program_name? CBL;
    program_program_name    : PROGRAM program_name?;

    ////////////////// names ////////////////////////////////////
    program_name            : name;


    ///////////////// common terms ///////////////////
    sign                    : PLUS | MINUS;
    letter_spec             : LETTER letter_range?;
    letter_range            : MINUS LETTER;
    name                    : LETTER IDENT_RE;

    ///////////////// regular expressions ////////////////////////////////////
    IDENT_RE                : /[_A-Z0-9]{{0,63}}/;
    PLUS                    : "+";
    MINUS                   : "-";
    EXPONENT_LETTER         : /[ED]/;
    DIGIT_STRING            : /[0-9]+/;
    LETTER                  : /[A-Z]/;
    REP_CHAR                : /{smapstr}/;
    CBL                     : CL | EOL;
    CL                      : C EOL;
    LBL                     : /[0-9]{{1,5}}/;
    C                       : /{cmapstr}/;
    EOL                     : /\r?\n/;

    ///////////////// keywords ////////////////////////////////////
    PROGRAM                 : "PROGRAM";
    END                     : "END";

    KEYWORD                 : /(PROGRAM|END)/;

    ///////////////// layout ////////////////////////////////////
    LAYOUT: LayoutItem | LAYOUT LayoutItem;
    LayoutItem: WS | EMPTY;
    WS: /[ \t]/;

""".format(
    smapstr=SMAPSTR.replace('%d', '[\d]+'),
    cmapstr=CMAPSTR.replace('%d', '[\d]+')
)

def transform(source, strmap={}, cmtmap={}):
    g = Grammar.from_string(f2003_grammar, ignore_case=True)
    #parser = Parser(g, build_tree=True)
    parser = GLRParser(g, build_tree=True)
    tree = parser.parse(source)
    import pdb; pdb.set_trace()
