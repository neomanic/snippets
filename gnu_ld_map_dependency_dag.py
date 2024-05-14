#!/usr/bin/env python3
"""
Take in a GNU ld map file and generate a dependency graph of the symbols, derived from the
cross-reference table at the end

These entries are of the form following, where the first column is the symbol name.
In the first row for each symbol, the second column is the object file (and library) where it's
defined. Succeeding rows are the object files where it's referenced.

PendSV_Handler                                    ../../lib/libqpc_qspy.a(qk_port.c.obj)
                                                  CMakeFiles/pullkey-biscuit462-qspy.dir/__/__/platform/startup_stm32l452xx.s.obj
QActive_ctor                                      ../../lib/libqpc_qspy.a(qf_qact.c.obj)
                                                  ../../lib/libqpc_qspy.a(qf_actq.c.obj)

"""

from collections import defaultdict
from dataclasses import dataclass, field
from functools import reduce
from os.path import basename
from pprint import pprint
import sys

from networkx import MultiDiGraph
from networkx.drawing.nx_pydot import write_dot
import networkx

@dataclass
class Reference:
    file: str
    object: str

@dataclass
class Symbol:
    name: str
    file: str
    object: str
    refs: list[Reference] = field(default_factory=list)

    @property
    def is_in_library(self):
        " Is this symbol defined in a library archive? False means a bare object file."
        return self.file.endswith(".a")

def lines_to_xrefs(lines):
    def xref_from_row(line):
        symbol = line.split()[0] if not line.startswith(" ") else None
        ref = line.split()[-1]
        # ref is split into file and object, if object separate, it's the basename of the file
        # ../../lib/libqpc_qspy.a(qf_ps.c.obj) -> 
        #              ../../lib/libqpc_qspy.a, qf_ps.c.obj
        # ../platform/startup_stm32l452xx.s.obj -> 
        #              ../platform/startup_stm32l452xx.s.obj, startup_stm32l452xx.s.obj
        ref_file = ref.split("(")[0].strip()
        ref_object = ref.split("(")[-1].strip("()") if "(" in ref else basename(ref_file)
        return (symbol, ref_file, ref_object)

    symbols = []
    current_symbol = None

    modules = MultiDiGraph()

    for line in f:
        if not line.strip(): # no empty lines until end of file
            break

        sym, ref_file, ref_object = xref_from_row(line)
        if sym: # new symbol
            current_symbol = Symbol(sym, ref_file, ref_object)
            symbols.append(current_symbol)
        else: # reference to current symbol
            current_symbol.refs.append(Reference(ref_file, ref_object))
            if current_symbol.file == ref_file: # don't link to self
                pass
            elif "qpc" in current_symbol.file or "qpc" in ref_file: # skip qpc
                pass
            elif networkx.is_path(modules, [ref_file, current_symbol.file]):
                pass
            else:
                modules.add_edge(ref_file, current_symbol.file) # , label=current_symbol.name

    return symbols, modules

def xrefs_to_file_deps(symbols, excludes=["arm-none-eabi"]):
    """Return a dict of file -> [files] dependencies for the given list of symbols."""
    file_deps = defaultdict(list)
    for sym in symbols:
        if any(ex in sym.file for ex in excludes):
            continue
        for ref in sym.refs:
            if any(ex in ref.file for ex in excludes):
                continue
            if ref.file not in file_deps:
                file_deps[ref.file] = []
            if sym.file not in file_deps[ref.file] and sym.file != ref.file:
                file_deps[ref.file].append(sym.file)
    return file_deps

def file_deps_to_dot(file_deps, extras=""):
    dot = "digraph G {\n"
    for file, deps in file_deps.items():
        for dep in deps:
            dot += f'"{file}" -> "{dep}";\n'
    dot += extras
    dot += "}"
    return dot

def xrefs_to_dot(symbols, exclude_libs=False, exclude_files=[]):
    """Turn a list[Symbol] into a graphviz dotfile.
    If `exclude_libs` is True, symbols originating in a library archive are not included.
    `exclude_files` can be used to avoid including useless info, eg the startup file
    """
    dot = "digraph G {\n"
    for sym in symbols:
        if not exclude_libs and sym.is_in_library:
            continue
        for ref in sym.refs:
            dot += f'"  {ref.object}" -> "{sym.name}";\n'

        #if sym.is_in_library:
        #    dot += f'"  {sym.symbol}" [shape=ellipse];\n'
        #else:
        #    dot += f'"  {sym.symbol}" [shape=box];\n'
    dot += "}"
    return dot

if __name__ == '__main__':
    assert sys.argv[1], "Please provide a map file"
    with open(sys.argv[1]) as f:
        # skip down to the cross-ref table, where the first 3 lines are:
        # Cross Reference Table
        # 
        # Symbol                                            File
        while not f.readline().strip() == "Cross Reference Table":
            continue
        assert f.readline().strip() == ""
        assert f.readline().strip().split() == ["Symbol", "File"]

        symbols, modules = lines_to_xrefs(f)

    file_deps = xrefs_to_file_deps(symbols)
    #pprint(file_deps)
    # deprefix
    prefixes = ["CMakeFiles/", "../../lib/"]
    deprefixer = lambda text, prefix: text.lstrip(prefix)
    cleaned_deps = {}
    app_files = []
    for filename, deps in file_deps.items():
        new_file = reduce(deprefixer, prefixes, filename)
        new_deps = [reduce(deprefixer, prefixes, dep) for dep in deps]
        cleaned_deps[new_file] = new_deps
        if ".dir" in new_file and new_file not in app_files:
            app_files.append(new_file)
        for dep in new_deps:
            if ".dir" in dep and dep not in app_files:
                app_files.append(dep)

    subgraph_nodes = ['"' + n + '";\n' for n in app_files]
    app_subgraph = "subgraph cluster_app {\n" + "".join(subgraph_nodes) + "}\n"

    #dot = file_deps_to_dot(cleaned_deps, app_subgraph)
    #print(dot)
    write_dot(modules, sys.argv[2])
    print("wrote to ", sys.argv[2])

        
    # we have our list of symbols... let's dotviz 'em
    # go with files to start


"""
    clusterrank=local;
    label="app";

    each archive becomes a cluster

        
"""
