import io
import dis
import contextlib
import builtins
from fuzzywuzzy import process, fuzz

SPELCHECK_MINSCORE = 75

old = builtins.__build_class__

CodeType = type((lambda: 0).__code__)


def new(body, name, *args, **kwargs):
    bases = args
    body.__code__ = spellcheck(body.__code__, globals=body.__globals__)
    return old(body, name, *bases, **kwargs)


builtins.__build_class__ = new


def new_code_from_old(code, **kwargs):
    args = [
        "co_argcount",
        "co_kwonlyargcount",
        "co_posonlyargcount",
        "co_nlocals",
        "co_stacksize",
        "co_flags",
        "co_code",
        "co_consts",
        "co_names",
        "co_varnames",
        "co_filename",
        "co_name",
        "co_firstlineno",
        "co_lnotab",
        "co_freevars",
        "co_cellvars",
    ]
    if not hasattr(code, "co_posonlyargcount"):
        args.remove("co_posonlyargcount")
    return CodeType(*(kwargs.get(arg, getattr(code, arg)) for arg in args))


def spellcheck(code, globals=globals()):
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        dis.dis(code)
    names = []
    for line in f.getvalue().split("\n"):
        if "LOAD_GLOBAL" in line:
            pre, LG, post = line.partition("LOAD_GLOBAL")
            pre, par, post = post.partition("(")
            names.append(post.rstrip(")"))
    available_names = set(globals) | set(code.co_varnames) | set(builtins.__dict__)
    misspelled = set(names) - available_names
    fixed, badglobals = {}, {}
    for wrong in misspelled:
        better, score = process.extractOne(
            wrong, available_names, scorer=fuzz.token_sort_ratio
        )
        if score < SPELCHECK_MINSCORE:
            continue
        fixed[wrong] = better
        if better not in globals and better not in builtins.__dict__:
            if wrong in code.co_names:
                badglobals[code.co_names.index(wrong)] = code.co_varnames.index(better)
    names = tuple(fixed.get(name, name) for name in code.co_names)

    bytecode = iter(code.co_code)
    bytecode_tmp = []
    for head in bytecode:
        tail = next(bytecode)
        if head == ord("t") and tail in badglobals:
            bytecode_tmp.append(ord("|"))
            bytecode_tmp.append(badglobals[tail])
        else:
            bytecode_tmp.extend([head, tail])
    bytecode = bytes(bytecode_tmp)

    functions = {
        val: spellcheck(val, globals=globals)
        for val in code.co_consts
        if isinstance(val, CodeType)
    }
    return new_code_from_old(
        code,
        co_consts=tuple(functions.get(const, const) for const in code.co_consts),
        co_names=names,
        co_code=bytecode,
    )
