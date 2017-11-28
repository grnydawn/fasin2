# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

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
