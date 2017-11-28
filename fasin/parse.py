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

#################################################
#  Classes
################################################
_cls_cache = {}

class Node(object):
    def __init__(self, children=[]):
        self.children = children

    def __str__(self):
        return ' '.join([str(c) for c in self.children if c])

#################################################
#  Rule actions
################################################
def tree_action_default_N(context, nodes):
    return tree_action_default(context, nodes, collect=lambda n: n[0])

def tree_action_default(context, nodes, collect=lambda n: n):
    if hasattr(context, 'symbol') and hasattr(context.symbol, 'name'):
        clsname = str(context.symbol.name)
        if clsname not in _cls_cache:
            _cls_cache[clsname] = type(clsname, (Node,), {})
        return _cls_cache[clsname](collect(nodes))
    else:
        return Node(collect(nodes))

def tree_action_join_space(context, nodes):
    return tree_action_join(context, nodes, sep=' ')

def tree_action_join(context, nodes, sep=''):
    return sep.join(nodes)

tree_actions = {
    "program": tree_action_default_N,
    "program_unit": tree_action_default,
    "main_program": tree_action_default,
    "end_program_stmt": tree_action_default,
    "program_program_name": tree_action_join_space,
    "name": tree_action_join
}

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
