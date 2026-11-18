"""Stubs of Blender's Python modules, written from their source.

The stubs keep what the source declares: imports, constants, classes with
their bases and decorators, dunders, annotations, dataclass and NamedTuple
fields, instance attributes and docstrings. They drop the function bodies.
Unlike the stubs made with inspect (gen_external_modules_modfile.py), they
lose nothing the source says.
"""

import ast
import json
import re
from pathlib import Path

# Written by gen_external_modules_modfile.py (SOURCE_MODULES_FILENAME there),
# which runs in Blender and cannot import this package.
SOURCE_MODULES_FILENAME = "source_modules.json"

# `bpy` is mostly C: its stub still comes from the API docs, which document
# its submodules but not the package itself. (`_bpy_types`, the Python half
# of `bpy.types`, is left out of source_modules.json by the modfile
# generator.)
DOCUMENTED_ELSEWHERE = {"bpy"}

MODULE_DIRECTIVE = re.compile(r"^\.\. (?:py:)?module:: (\S+)\s*$", re.MULTILINE)

FunctionDef = ast.FunctionDef | ast.AsyncFunctionDef
FUNCTION_DEFS = (ast.FunctionDef, ast.AsyncFunctionDef)
DEFINITIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)

LITERAL_TYPES = (bool, int, float, str, bytes)
# `type X = ...` (Python 3.12+).
TYPE_ALIAS = (ast.TypeAlias,) if hasattr(ast, "TypeAlias") else ()
DECLARATIONS = (ast.Import, ast.ImportFrom, *TYPE_ALIAS, ast.Pass)
ASSIGNMENTS = (ast.Assign, ast.AugAssign, ast.AnnAssign)


def _ellipsis() -> ast.stmt:
    return ast.Expr(ast.Constant(...))


class _TypingImport:

    """Whether a stub refers to ``typing``, so that it must import it.

    An attribute of unknown type is ``typing.Any``.
    """

    def __init__(self) -> None:
        self.needed = False


def _strip_body(func: FunctionDef) -> None:
    body: list[ast.stmt] = []
    if ast.get_docstring(func, clean=False) is not None:
        body.append(func.body[0])
    body.append(_ellipsis())
    func.body = body


def _declared_names(body: list[ast.stmt]) -> set[str]:
    names: set[str] = set()
    for stmt in body:
        if isinstance(stmt, DEFINITIONS):
            names.add(stmt.name)
        elif isinstance(stmt, ast.AnnAssign):
            if isinstance(stmt.target, ast.Name):
                names.add(stmt.target.id)
        elif isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                names.update(n.id for n in ast.walk(target)
                             if isinstance(n, ast.Name))
    return names


def _decorator_name(decorator: ast.expr) -> str:
    if isinstance(decorator, ast.Call):
        decorator = decorator.func
    if isinstance(decorator, ast.Attribute):
        return decorator.attr
    if isinstance(decorator, ast.Name):
        return decorator.id
    return ""


def _self_name(func: FunctionDef) -> str | None:
    decorators = {_decorator_name(d) for d in func.decorator_list}
    if decorators & {"staticmethod", "classmethod"}:
        return None
    args = func.args.posonlyargs + func.args.args
    return args[0].arg if args else None


def _has_synthesized_init(cls: ast.ClassDef) -> bool:
    """Tell whether every class-level annotation of ``cls`` is a field.

    A dataclass or a NamedTuple takes each one as an ``__init__`` parameter.
    """
    if any(_decorator_name(d) == "dataclass" for d in cls.decorator_list):
        return True
    return any(_decorator_name(b) == "NamedTuple" for b in cls.bases)


def _value_type(value: ast.expr, func: FunctionDef) -> str | None:
    """Return the type of an attribute ``func`` assigns ``value``.

    The type is source text, or None if unknown: a literal gives its type,
    a parameter its annotation.
    """
    if isinstance(value, ast.Constant):
        if value.value is None:
            return "None"
        if isinstance(value.value, LITERAL_TYPES):
            return type(value.value).__name__
        return None
    if isinstance(value, ast.Name):
        args = func.args
        for arg in args.posonlyargs + args.args + args.kwonlyargs:
            if arg.arg == value.id and arg.annotation is not None:
                return ast.unparse(arg.annotation)
    return None


def _bound_targets(target: ast.expr) -> list[ast.expr]:
    """List what an assignment to ``target`` binds, through tuple unpacking.

    In ``self.a.b = x`` that is ``self.a.b``, not ``self.a``.
    """
    if isinstance(target, (ast.Tuple, ast.List)):
        return [t for e in target.elts for t in _bound_targets(e)]
    if isinstance(target, ast.Starred):
        return _bound_targets(target.value)
    return [target]


def _self_assignments(
        func: FunctionDef, self_name: str
) -> list[tuple[str, str | None, bool]]:
    """List what ``func`` assigns on ``self``: (name, type, annotated)."""
    found = []
    for node in ast.walk(func):
        if isinstance(node, ast.AnnAssign):
            pairs = [(node.target, node.value)]
        elif isinstance(node, ast.Assign):
            pairs = [(t, node.value) for t in node.targets]
        else:
            continue
        for target, value in pairs:
            for sub in _bound_targets(target):
                if not (isinstance(sub, ast.Attribute)
                        and isinstance(sub.value, ast.Name)
                        and sub.value.id == self_name):
                    continue
                if isinstance(node, ast.AnnAssign):
                    found.append(
                        (sub.attr, ast.unparse(node.annotation), True))
                elif sub is target:
                    found.append((sub.attr, _value_type(value, func), False))
                else:
                    found.append((sub.attr, None, False))
    return found


def _instance_attributes(cls: ast.ClassDef) -> dict[str, str | None]:
    """Return the attributes the methods of ``cls`` assign on ``self``.

    Each comes with its type: its annotation, the union of the types of its
    values, or None if one of them is unknown.
    """
    types: dict[str, list[str | None]] = {}
    annotated: dict[str, str] = {}
    for func in cls.body:
        if not isinstance(func, FUNCTION_DEFS):
            continue
        self_name = _self_name(func)
        if self_name is None:
            continue
        for name, type_, is_annotation in _self_assignments(func, self_name):
            types.setdefault(name, [])
            if is_annotation:
                annotated.setdefault(name, type_)
            else:
                types[name].append(type_)
    result: dict[str, str | None] = {}
    for name, found in types.items():
        if name in annotated:
            result[name] = annotated[name]
        elif None in found:
            result[name] = None
        else:
            result[name] = " | ".join(dict.fromkeys(found))
    return result


def _stub_class(cls: ast.ClassDef, typing_import: _TypingImport) -> None:
    attributes = {}
    if not _has_synthesized_init(cls):
        attributes = _instance_attributes(cls)
    cls.body = _stub_body(cls.body, typing_import)
    declared = _declared_names(cls.body)
    insert_at = 0
    while insert_at < len(cls.body) and \
            not isinstance(cls.body[insert_at], DEFINITIONS):
        insert_at += 1
    new: list[ast.stmt] = []
    for name, type_ in attributes.items():
        if name in declared:
            continue
        annotation = type_
        if annotation is None:
            typing_import.needed = True
            annotation = "typing.Any"
        new.append(ast.AnnAssign(
            target=ast.Name(name),
            annotation=ast.parse(annotation, mode="eval").body,
            value=None, simple=1))
    cls.body[insert_at:insert_at] = new
    if not cls.body:
        cls.body = [_ellipsis()]


def _binds_names(target: ast.expr) -> bool:
    if isinstance(target, ast.Name):
        return True
    if isinstance(target, (ast.Tuple, ast.List)):
        return all(_binds_names(e) for e in target.elts)
    if isinstance(target, ast.Starred):
        return _binds_names(target.value)
    return False


def _is_main_guard(stmt: ast.If) -> bool:
    test = stmt.test
    return (isinstance(test, ast.Compare)
            and isinstance(test.left, ast.Name)
            and test.left.id == "__name__"
            and len(test.comparators) == 1
            and isinstance(test.comparators[0], ast.Constant)
            and test.comparators[0].value == "__main__")


def _is_docstring(stmt: ast.stmt) -> bool:
    return (isinstance(stmt, ast.Expr)
            and isinstance(stmt.value, ast.Constant)
            and isinstance(stmt.value.value, str))


def _stub_block(statements: list[ast.stmt],
                typing_import: _TypingImport) -> list[ast.stmt]:
    """Stub a block nested in ``if`` or ``try``, which is never empty."""
    return _stub_body(statements, typing_import) or [_ellipsis()]


def _stub_statement(stmt: ast.stmt, typing_import: _TypingImport) -> bool:
    """Stub ``stmt`` in place; return whether the stub keeps it."""
    if isinstance(stmt, FUNCTION_DEFS):
        _strip_body(stmt)
    elif isinstance(stmt, ast.ClassDef):
        _stub_class(stmt, typing_import)
    elif isinstance(stmt, ast.If):
        if _is_main_guard(stmt):
            return False
        stmt.body = _stub_block(stmt.body, typing_import)
        stmt.orelse = _stub_body(stmt.orelse, typing_import)
    elif isinstance(stmt, (ast.Try, ast.TryStar)):
        stmt.body = _stub_block(stmt.body, typing_import)
        for handler in stmt.handlers:
            handler.body = _stub_block(handler.body, typing_import)
        stmt.orelse = _stub_body(stmt.orelse, typing_import)
        stmt.finalbody = _stub_body(stmt.finalbody, typing_import)
    elif isinstance(stmt, ASSIGNMENTS):
        # Setting an attribute or an item declares nothing.
        targets = stmt.targets if isinstance(stmt, ast.Assign) \
            else [stmt.target]
        return all(_binds_names(t) for t in targets)
    else:
        return isinstance(stmt, DECLARATIONS)
    return True


def _stub_body(statements: list[ast.stmt],
               typing_import: _TypingImport) -> list[ast.stmt]:
    """Keep the declarations among ``statements``.

    These are the imports, the assignments to names, the classes and
    functions (without their bodies), and the ``if`` and ``try`` blocks
    around them. A docstring stays; other expressions, loops, ``with`` and
    ``del`` go.
    """
    kept: list[ast.stmt] = []
    for index, stmt in enumerate(statements):
        if ((index == 0 and _is_docstring(stmt))
                or _stub_statement(stmt, typing_import)):
            kept.append(stmt)
    return kept


def _imports_typing(module: ast.Module) -> bool:
    return any(
        isinstance(stmt, ast.Import)
        and any(a.name == "typing" and a.asname is None for a in stmt.names)
        for stmt in module.body)


def _insert_typing_import(module: ast.Module) -> None:
    position = 0
    if ast.get_docstring(module, clean=False) is not None:
        position = 1
    while position < len(module.body):
        stmt = module.body[position]
        if not (isinstance(stmt, ast.ImportFrom)
                and stmt.module == "__future__"):
            break
        position += 1
    module.body.insert(position, ast.Import(names=[ast.alias("typing")]))


def make_stub(source: str, *, as_package: bool = False) -> str:
    """Return the stub (``.pyi`` text) of the Python module ``source``.

    With ``as_package``, the stub of a plain module goes in a package's
    ``__init__.pyi`` (fake-bpy-module's layout), so its relative imports go
    up one level more.
    """
    module = ast.parse(source)
    if as_package:
        for node in ast.walk(module):
            if isinstance(node, ast.ImportFrom) and node.level > 0:
                node.level += 1
    typing_import = _TypingImport()
    module.body = _stub_body(module.body, typing_import)
    if typing_import.needed and not _imports_typing(module):
        _insert_typing_import(module)
    return ast.unparse(module) + "\n"


def documented_modules(target_files: list[str]) -> set[str]:
    """Return the modules the API docs ``target_files`` document."""
    modules = set()
    for f in target_files:
        modules.update(MODULE_DIRECTIVE.findall(
            Path(f).read_text(encoding="utf-8", errors="replace")))
    return modules


def source_module_files(generated_mods_dir: Path) -> dict[str, Path]:
    """Return the source file of each Python module listed for source stubs.

    The modfile generator lists them under ``generated_mods_dir``.
    """
    module_files = {}
    for p in sorted(Path(generated_mods_dir).rglob(SOURCE_MODULES_FILENAME)):
        module_files.update(json.loads(p.read_text(encoding="utf-8")))
    return module_files


def write_stubs(module_files: dict[str, Path], documented: set[str],
                output_dir: Path) -> list[str]:
    """Write the stubs of the Python modules ``module_files`` from source.

    ``module_files`` maps each module name to its source file. The stubs go
    in fake-bpy-module's layout (``<top>-stubs/<sub>/__init__.pyi``) under
    ``output_dir``, over what the API docs pipeline wrote for them. The
    modules the API docs document (``documented``) keep the stubs made from
    the docs. Returns the names of the modules written.
    """
    written = []
    for name in sorted(module_files):
        if name in documented or name in DOCUMENTED_ELSEWHERE:
            continue
        source_file = Path(module_files[name])
        is_package = source_file.name == "__init__.py"
        parts = name.split(".")
        top = Path(output_dir, f"{parts[0]}-stubs")
        stub_dir = top.joinpath(*parts[1:])
        stub_dir.mkdir(parents=True, exist_ok=True)
        stub = make_stub(source_file.read_text(encoding="utf-8"),
                         as_package=not is_package)
        (stub_dir / "__init__.pyi").write_text(
            stub, encoding="utf-8", newline="\n")
        (top / "py.typed").touch()
        written.append(name)
    return written
