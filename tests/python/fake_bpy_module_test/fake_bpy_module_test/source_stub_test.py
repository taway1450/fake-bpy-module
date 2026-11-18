import tempfile
import textwrap
from pathlib import Path

from fake_bpy_module.source_stub import (  # pylint: disable=E0401
    make_stub,
    write_stubs,
)

from . import common


def dedent(text: str) -> str:
    return textwrap.dedent(text).lstrip("\n")


class SourceStubTest(common.FakeBpyModuleTestBase):

    name = "SourceStubTest"
    module_name = __module__

    def test_function_keeps_signature_and_docstring(self) -> None:
        source = dedent("""
            def path_split(path: str, *, sep="/") -> list[str]:
                \"\"\"Split a path.\"\"\"
                parts = path.split(sep)
                return parts
            """)
        expect = dedent("""
            def path_split(path: str, *, sep='/') -> list[str]:
                \"\"\"Split a path.\"\"\"
                ...
            """)

        self.assertEqual(expect, make_stub(source))

    def test_instance_attributes_are_declared_on_the_class(self) -> None:
        source = dedent("""
            import typing


            class Report:
                kind: str

                def __init__(self, path: str, count, kind):
                    self.path = path
                    self.count = 0
                    self.kind = kind
                    self.error = None

                def fail(self, message):
                    self.error = message
                    self.count += 1
            """)
        expect = dedent("""
            import typing

            class Report:
                kind: str
                path: str
                count: int
                error: typing.Any

                def __init__(self, path: str, count, kind):
                    ...

                def fail(self, message):
                    ...
            """)

        self.assertEqual(expect, make_stub(source))

    def test_typing_is_imported_for_untyped_attributes(self) -> None:
        source = dedent("""
            class Report:
                def __init__(self, data):
                    self.data = data
                    self.ok: bool = True
            """)
        expect = dedent("""
            import typing

            class Report:
                data: typing.Any
                ok: bool

                def __init__(self, data):
                    ...
            """)

        self.assertEqual(expect, make_stub(source))

    def test_module_keeps_declarations_and_drops_statements(self) -> None:
        source = dedent("""
            \"\"\"Module docstring.\"\"\"
            import os
            from typing import TYPE_CHECKING
            if TYPE_CHECKING:
                from pathlib import Path
            try:
                import numpy
            except ImportError:
                numpy = None
            API_VERSION = "v1"
            error_duplicates = []
            __all__ = ["main"]
            __all__ += ["other"]
            print("loading")
            for name in ("a", "b"):
                globals()[name] = name
            with open(os.devnull) as fh:
                pass
            del os
            if __name__ == "__main__":
                main()
            """)
        expect = dedent("""
            \"\"\"Module docstring.\"\"\"
            import os
            from typing import TYPE_CHECKING
            if TYPE_CHECKING:
                from pathlib import Path
            try:
                import numpy
            except ImportError:
                numpy = None
            API_VERSION = 'v1'
            error_duplicates = []
            __all__ = ['main']
            __all__ += ['other']
            """)

        self.assertEqual(expect, make_stub(source))

    def test_module_stubbed_as_package_keeps_relative_imports(self) -> None:
        source = dedent("""
            from . import sibling
            from .common import ToolDef
            from os import path
            """)
        expect = dedent("""
            from .. import sibling
            from ..common import ToolDef
            from os import path
            """)

        self.assertEqual(expect, make_stub(source, as_package=True))


    def test_assignments_to_attributes_and_items_are_dropped(self) -> None:
        source = dedent("""
            def modules():
                pass
            modules._is_first = True
            table = {}
            table["a"] = 1
            a, (b, c) = 1, (2, 3)
            """)
        expect = dedent("""
            def modules():
                ...
            table = {}
            a, (b, c) = (1, (2, 3))
            """)

        self.assertEqual(expect, make_stub(source))


    def test_dataclass_fields_stay_the_only_fields(self) -> None:
        source = dedent("""
            import dataclasses
            @dataclasses.dataclass
            class FileV1:
                path: str
                size: int = 0
                tags: list = dataclasses.field(default_factory=list)

                def __post_init__(self):
                    self.checked = False
            """)
        expect = dedent("""
            import dataclasses

            @dataclasses.dataclass
            class FileV1:
                path: str
                size: int = 0
                tags: list = dataclasses.field(default_factory=list)

                def __post_init__(self):
                    ...
            """)

        self.assertEqual(expect, make_stub(source))


    def test_setting_a_member_of_an_attribute_declares_nothing(self) -> None:
        source = dedent("""
            class Panel:
                def draw(self, context):
                    self.layout.use_property_split = True
                    self.items[0] = 1
                    self.a, (self.b, *self.c) = 1, (2, 3)
            """)
        expect = dedent("""
            import typing

            class Panel:
                a: typing.Any
                b: typing.Any
                c: typing.Any

                def draw(self, context):
                    ...
            """)

        self.assertEqual(expect, make_stub(source))


class WriteStubsTest(common.FakeBpyModuleTestBase):

    name = "WriteStubsTest"
    module_name = __module__

    def test_writes_undocumented_modules_in_the_stub_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            src = Path(tmp, "scripts")
            files = {
                "bl_ui": src / "bl_ui" / "__init__.py",
                "bl_ui.utils": src / "bl_ui" / "utils.py",
                "addon_utils": src / "addon_utils.py",
                "bpy_extras.io_utils": src / "bpy_extras" / "io_utils.py",
                "bpy": src / "bpy" / "__init__.py",
            }
            contents = {
                "bl_ui": "from . import utils\n",
                "bl_ui.utils": "from . import x\nX = 1\n",
                "addon_utils": "paths = []\n",
                "bpy_extras.io_utils": "Y = 1\n",
                "bpy": "Z = 1\n",
            }
            for name, path in files.items():
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(contents[name])
            out = Path(tmp, "out")
            documented = out / "bpy_extras-stubs" / "io_utils" / "__init__.pyi"
            documented.parent.mkdir(parents=True)
            documented.write_text("documented\n")

            written = write_stubs(files, {"bpy_extras.io_utils"}, out)

            def stub(*parts: str) -> str:
                return out.joinpath(*parts, "__init__.pyi").read_text()

            self.assertEqual(["addon_utils", "bl_ui", "bl_ui.utils"], written)
            self.assertEqual("from . import utils\n", stub("bl_ui-stubs"))
            self.assertEqual("from .. import x\nX = 1\n",
                             stub("bl_ui-stubs", "utils"))
            self.assertEqual("paths = []\n", stub("addon_utils-stubs"))
            self.assertTrue((out / "addon_utils-stubs" / "py.typed").exists())
            self.assertEqual("documented\n", documented.read_text())
            self.assertFalse((out / "bpy-stubs").exists())
