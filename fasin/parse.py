# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
import os, re
from .util import fixedform_extensions, CMAPSTR, SMAPSTR
from parglare import Parser, GLRParser, Grammar
from .tree_actions import tree_actions

f2003_grammar = r"""
    // Fortran2003 grammar specification excerpt from J3/04-007
    // __version__ : 0.1.0

    ///////////////// Fortran high-level concepts /////////////////
    program                 : program_unit+;
    program_unit            : main_program | CBL;
    main_program            : end_program_stmt;
    //main_program            : program_stmt? specification_part? execution_part?
    //                          internal_subprogram_part? end_program_stmt;



    ///////////////// end statements ///////////////////////////////
    end_program_stmt        : LABEL? END program_program_name? CBL;
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
    LABEL                   : /[0-9]{{1,5}}/;
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

def transform(source, strmap={}, cmtmap={}, output="tree"):

    parser_class = Parser #GLRParser # Parser
    actions = globals().get('%s_actions'%output, None)
    layout_actions = globals().get('%s_layout_actions'%output, None)
    assert actions, "%s actions do not supported."%output

    g = Grammar.from_string(f2003_grammar, ignore_case=True)
    parser = parser_class(g, build_tree=True, actions=actions,
        debug=True, debug_colors=True)
    parsed = parser.parse(source)
    #tree = parser.call_actions(parsed[0])
    tree = parser.call_actions(parsed)
    import pdb; pdb.set_trace()
    return tree
