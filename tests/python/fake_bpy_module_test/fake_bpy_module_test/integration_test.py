import shutil
import textwrap
from pathlib import Path

from fake_bpy_module import config  # pylint: disable=E0401
from fake_bpy_module.analyzer.analyzer import analyze  # pylint: disable=E0401
from fake_bpy_module.generator.generator import (
    generate,  # pylint: disable=E0401
)
from fake_bpy_module.transformer.transformer import (
    transform,  # pylint: disable=E0401
)

from . import common


class IntegrationTest(common.FakeBpyModuleTestBase):

    name = "IntegrationTest"
    module_name = __module__
    data_dir = Path(
        f"{Path(__file__).parent}/integration_test_data/integration_test").resolve()

    def setUp(self) -> None:
        super().setUp()

        self.output_dir = "fake_bpy_module_test_tmp"
        self.output_file_path = f"{self.output_dir}/integration_test_output"
        Path(self.output_dir).mkdir(parents=True, exist_ok=False)

        self.__setup_config()

    def tearDown(self) -> None:
        super().tearDown()

        shutil.rmtree(self.output_dir)

    def __setup_config(self) -> None:
        config.set_output_dir(self.output_dir)
        config.set_os("Linux")
        config.set_style_format("ruff")
        config.set_target("blender")
        config.set_target_version("2.80")
        config.set_mod_version("2.80")

    def __is_py_typed_exist(self, filepath: str) -> bool:
        if not Path(filepath).is_file():
            return False
        return Path(filepath).stat().st_size == 0

    def test_single(self) -> None:
        rst_files = [
            f"{self.data_dir}/input/single/module_abc.rst",
        ]

        ext_patterns = ["py", "pyi"]
        for ext in ext_patterns:
            config.set_output_format(ext)
            documents = analyze(rst_files)
            documents = transform(documents, [])
            generate(documents)

            expect_files_dir = f"{self.data_dir}/expect/single"
            actual_files_dir = self.output_dir

            py_files = [
                f"module_abc-stubs/__init__.{ext}",
            ]
            for file_ in py_files:
                expect_file_path = f"{expect_files_dir}/{file_}"
                actual_file_path = f"{actual_files_dir}/{file_}"
                with Path(actual_file_path).open("r", encoding="utf-8") as f:
                    expect_contents = f.read()
                with Path(expect_file_path).open("r", encoding="utf-8") as f:
                    actual_contents = f.read()
                self.log(
                    f"============= Expect: {expect_file_path} =============")
                self.log(expect_contents)
                self.log(
                    f"============= Actual: {actual_file_path} =============")
                self.log(actual_contents)
                self.assertEqual(expect_contents, actual_contents)

            self.assertFalse(self.__is_py_typed_exist(f"{self.output_dir}/py.typed"))

    def test_multiple(self) -> None:
        rst_files = [
            f"{self.data_dir}/input/multiple/module_1.rst",
            f"{self.data_dir}/input/multiple/module_1.submodule_1.rst",
            f"{self.data_dir}/input/multiple/module_2.rst",
            f"{self.data_dir}/input/multiple/rna_enum_enum1.rst",
        ]

        ext_patterns = ["py", "pyi"]
        for ext in ext_patterns:
            config.set_output_format(ext)
            documents = analyze(rst_files)
            documents = transform(documents, [])
            generate(documents)

            expect_files_dir = f"{self.data_dir}/expect/multiple"
            actual_files_dir = self.output_dir

            py_files = [
                f"module_1-stubs/__init__.{ext}",
                f"module_1-stubs/submodule_1/__init__.{ext}",
                f"module_2-stubs/__init__.{ext}",
            ]
            for file_ in py_files:
                expect_file_path = f"{expect_files_dir}/{file_}"
                actual_file_path = f"{actual_files_dir}/{file_}"
                with Path(actual_file_path).open("r", encoding="utf-8") as f:
                    expect_contents = f.read()
                with Path(expect_file_path).open("r", encoding="utf-8") as f:
                    actual_contents = f.read()
                self.log(
                    f"============= Expect: {expect_file_path} =============")
                self.log(expect_contents)
                self.log(
                    f"============= Actual: {actual_file_path} =============")
                self.log(actual_contents)
                self.assertEqual(expect_contents, actual_contents)

            self.assertFalse(self.__is_py_typed_exist(f"{self.output_dir}/py.typed"))

    def test_exceptional(self) -> None:
        rst_files = [
            f"{self.data_dir}/input/exceptional/module_exceptional.rst",
        ]

        ext_patterns = ["py", "pyi"]
        for ext in ext_patterns:
            config.set_output_format(ext)
            documents = analyze(rst_files)
            documents = transform(documents, [])
            generate(documents)

            expect_files_dir = f"{self.data_dir}/expect/exceptional"
            actual_files_dir = self.output_dir

            py_files = [
                f"module_exceptional-stubs/__init__.{ext}",
            ]
            for file_ in py_files:
                expect_file_path = f"{expect_files_dir}/{file_}"
                actual_file_path = f"{actual_files_dir}/{file_}"
                with Path(actual_file_path).open("r", encoding="utf-8") as f:
                    expect_contents = f.read()
                with Path(expect_file_path).open("r", encoding="utf-8") as f:
                    actual_contents = f.read()
                self.log(
                    f"============= Expect: {expect_file_path} =============")
                self.log(expect_contents)
                self.log(
                    f"============= Actual: {actual_file_path} =============")
                self.log(actual_contents)
                self.assertEqual(expect_contents, actual_contents)

            self.assertFalse(self.__is_py_typed_exist(f"{self.output_dir}/py.typed"))

    def test_class_alias(self) -> None:
        # Blender registers the classes of its Python modules in bpy.types:
        # bpy.types.ClassA is module_1.ClassA itself, not an instance of it.
        input_dir = Path(self.output_dir) / "input"
        input_dir.mkdir()
        (input_dir / "module_1.rst").write_text(textwrap.dedent("""\
            .. module:: module_1

            .. class:: ClassA

               .. method:: execute(context)

                  :type context: int
            """), encoding="utf-8")
        (input_dir / "module_2.rst").write_text(textwrap.dedent("""\
            .. module:: module_2

            .. class:: ClassA

            .. data:: ClassA

               :type: :class:`module_1.ClassA`
               :option data: class-alias
            """), encoding="utf-8")

        config.set_output_format("pyi")
        documents = analyze([str(input_dir / "module_1.rst"),
                             str(input_dir / "module_2.rst")])
        documents = transform(documents, [])
        generate(documents)

        stub = (Path(self.output_dir) / "module_2-stubs" / "__init__.pyi"
                ).read_text(encoding="utf-8")
        self.log(stub)
        self.assertIn("ClassA = module_1.ClassA\n", stub)
        self.assertNotIn("class ClassA", stub)
        self.assertNotIn("ClassA:", stub)

    def test_orphan_page(self) -> None:
        # Sphinx reads ":orphan:" before a page's title as file-wide metadata.
        # Blender's API docs mark the type-checker-only views so
        # (bpy.types._Object_MESH), and their classes belong in the stubs.
        input_dir = Path(self.output_dir) / "input"
        input_dir.mkdir()
        (input_dir / "module_1.ClassA.rst").write_text(textwrap.dedent("""\
            ClassA
            ======

            .. currentmodule:: module_1

            .. class:: ClassA

               .. attribute:: kind

                  :type: str
            """), encoding="utf-8")
        (input_dir / "module_1._ClassA_X.rst").write_text(textwrap.dedent("""\
            :orphan:

            _ClassA_X
            =========

            .. currentmodule:: module_1

            .. class:: _ClassA_X

               A ClassA whose kind is 'X'.

               .. attribute:: kind

                  :type: Literal['X']
            """), encoding="utf-8")

        config.set_output_format("pyi")
        documents = analyze([str(input_dir / "module_1.ClassA.rst"),
                             str(input_dir / "module_1._ClassA_X.rst")])
        documents = transform(documents, [])
        generate(documents)

        stub = (Path(self.output_dir) / "module_1-stubs" / "__init__.pyi"
                ).read_text(encoding="utf-8")
        self.log(stub)
        self.assertIn("class ClassA:", stub)
        self.assertIn("class _ClassA_X:", stub)

    def test_class_signature_bases(self) -> None:
        # Blender's API docs name a class's bases in its signature, as a
        # class statement does. A "base classes" line, where a page has one,
        # lists every base and wins.
        input_dir = Path(self.output_dir) / "input"
        input_dir.mkdir()
        (input_dir / "module_1.rst").write_text(textwrap.dedent("""\
            .. module:: module_1

            .. class:: BaseA

            .. class:: BaseB

            .. class:: ClassA(BaseA, BaseB)

            .. class:: ClassB(arg_1)

               :arg arg_1: Argument 1.
               :type arg_1: int

            .. class:: ClassC(BaseB, metaclass=type)
            """), encoding="utf-8")
        (input_dir / "module_1.ClassD.rst").write_text(textwrap.dedent("""\
            ClassD(BaseB)
            =============

            .. currentmodule:: module_1

            base classes --- :class:`BaseA`, :class:`BaseB`

            .. class:: ClassD(BaseB)
            """), encoding="utf-8")

        config.set_output_format("pyi")
        documents = analyze([str(input_dir / "module_1.rst"),
                             str(input_dir / "module_1.ClassD.rst")])
        documents = transform(documents, [])
        generate(documents)

        stub = (Path(self.output_dir) / "module_1-stubs" / "__init__.pyi"
                ).read_text(encoding="utf-8")
        self.log(stub)
        self.assertIn("class ClassA(BaseA, BaseB):", stub)
        self.assertIn("class ClassB:", stub)
        self.assertIn("def __init__(self, arg_1: int)", stub)
        self.assertIn("class ClassC(BaseB):", stub)
        self.assertIn("class ClassD(BaseB, BaseA):", stub)

    def test_redeclared_pointer(self) -> None:
        # A bpy.types pointer can be None unless the docs flag it never None.
        # A class that redeclares a pointer of its base narrows it, and its
        # type says whether None remains (bpy.types._Object_MESH.data).
        input_dir = Path(self.output_dir) / "input"
        input_dir.mkdir()
        (input_dir / "bpy.types.ClassA.rst").write_text(textwrap.dedent("""\
            ClassA
            ======

            .. currentmodule:: bpy.types

            .. class:: ClassA

               .. attribute:: data

                  :type: :class:`ClassB` | None

               .. attribute:: other

                  :type: :class:`ClassB`

            .. class:: ClassB
            """), encoding="utf-8")
        (input_dir / "bpy.types._ClassA_X.rst").write_text(textwrap.dedent("""\
            :orphan:

            _ClassA_X
            =========

            .. currentmodule:: bpy.types

            .. class:: _ClassA_X(ClassA)

               .. attribute:: data

                  :type: :class:`ClassB`

               .. attribute:: other

                  :type: :class:`ClassB` | None
            """), encoding="utf-8")

        config.set_output_format("pyi")
        documents = analyze([str(input_dir / "bpy.types.ClassA.rst"),
                             str(input_dir / "bpy.types._ClassA_X.rst")])
        documents = transform(documents, [])
        generate(documents)

        stub = (Path(self.output_dir) / "bpy-stubs" / "types" / "__init__.pyi"
                ).read_text(encoding="utf-8")
        self.log(stub)
        view = stub[stub.index("class _ClassA_X(ClassA):"):]
        self.assertIn("    data: ClassB  #", view)
        self.assertIn("    other: ClassB | None\n", view)

    def test_collection_of_union(self) -> None:
        # A collection whose items are one of several classes
        # (GreasePencil.root_nodes holds layers and layer groups).
        input_dir = Path(self.output_dir) / "input"
        input_dir.mkdir()
        (input_dir / "bpy.types.ClassA.rst").write_text(textwrap.dedent("""\
            ClassA
            ======

            .. currentmodule:: bpy.types

            .. class:: bpy_prop_collection

            .. class:: ClassA

               .. data:: items

                  (readonly)

                  :type: UNION_COLLECTION

               .. data:: single

                  (readonly)

                  :type: :class:`bpy_prop_collection`\\ [:class:`ClassB`]

            .. class:: ClassB

            .. class:: ClassC
            """).replace(
                "UNION_COLLECTION",
                ":class:`bpy_prop_collection`\\ "
                "[:class:`ClassB` | :class:`ClassC`]"), encoding="utf-8")

        config.set_output_format("pyi")
        documents = analyze([str(input_dir / "bpy.types.ClassA.rst")])
        documents = transform(documents, [])
        generate(documents)

        stub = (Path(self.output_dir) / "bpy-stubs" / "types" / "__init__.pyi"
                ).read_text(encoding="utf-8")
        self.log(stub)
        self.assertIn("bpy_prop_collection[ClassB]", stub)
        self.assertIn("bpy_prop_collection[ClassB | ClassC]", stub)
