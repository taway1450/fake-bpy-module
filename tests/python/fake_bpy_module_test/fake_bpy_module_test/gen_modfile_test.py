import importlib.util
import sys
import tempfile
import types
from pathlib import Path

import fake_bpy_module  # pylint: disable=E0401

from . import common

GEN_MODFILE_DIR = Path(fake_bpy_module.__file__).parents[1] / "gen_modfile"


def load_gen_external_modules_modfile(
        bpy_types_names: list[str]) -> types.ModuleType:
    """Load gen_external_modules_modfile.py with a stand-in for Blender's bpy.

    ``bpy_types_names`` are the names Blender registers in ``bpy.types``.
    """
    bpy = types.ModuleType("bpy")
    bpy.types = types.SimpleNamespace(**dict.fromkeys(bpy_types_names))
    saved_bpy = sys.modules.get("bpy")
    sys.modules["bpy"] = bpy
    try:
        path = GEN_MODFILE_DIR / "gen_external_modules_modfile.py"
        spec = importlib.util.spec_from_file_location(
            "gen_external_modules_modfile", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    finally:
        if saved_bpy is None:
            del sys.modules["bpy"]
        else:
            sys.modules["bpy"] = saved_bpy
    return module


def fake_module(name: str, source: str) -> types.ModuleType:
    module = types.ModuleType(name)
    exec(source, module.__dict__)  # noqa: S102
    sys.modules[name] = module
    return module


class GenExternalModulesModfileTest(common.FakeBpyModuleTestBase):

    name = "GenExternalModulesModfileTest"
    module_name = __module__

    def setUp(self) -> None:
        super().setUp()
        self.addCleanup(sys.modules.pop, "_bpy_types", None)
        self.addCleanup(sys.modules.pop, "module_1", None)

    def write_modfiles(self, gen: types.ModuleType,
                       results: dict) -> dict[str, str]:
        with tempfile.TemporaryDirectory() as output_dir:
            config = gen.GenerationConfig()
            config.output_dir = output_dir
            config.output_format = "rst"
            gen.write_to_modfile(results, config)
            return {p.name: p.read_text(encoding="utf-8")
                    for p in Path(output_dir).iterdir()}

    def test_registered_class_is_a_class_alias_in_bpy_types(self) -> None:
        gen = load_gen_external_modules_modfile(["ClassA"])
        module_1 = fake_module("module_1", "class ClassA:\n    pass\n")
        results = gen.analyze([{"module_name": "module_1",
                                "module": module_1}])
        results["bpy.types"] = gen.get_alias_to_bpy_types(results)

        modfile = self.write_modfiles(gen, results)["bpy.types.mod.rst"]

        self.log(modfile)
        self.assertIn(".. data:: ClassA\n\n"
                      "   :type: :class:`module_1.ClassA`\n"
                      "   :option data: class-alias\n", modfile)

    def test_bpy_types_python_half_maps_to_bpy_types(self) -> None:
        # Blender 5.0 renamed bpy_types to _bpy_types. Its classes are the
        # Python half of bpy.types: other modules subclass them as
        # bpy.types.X, and _bpy_types keeps only _GenericUI.
        gen = load_gen_external_modules_modfile(["Menu"])
        bpy_types = fake_module("_bpy_types", (
            "class _GenericUI:\n    pass\n"
            "class Menu(_GenericUI):\n    pass\n"))
        module_1 = fake_module("module_1", (
            "import _bpy_types\n"
            "class MY_MT_menu(_bpy_types.Menu):\n    pass\n"))

        results = gen.analyze([
            {"module_name": "_bpy_types", "module": bpy_types},
            {"module_name": "module_1", "module": module_1},
        ])

        self.assertEqual(
            ["_GenericUI"],
            [c["name"] for c in results["_bpy_types"]["classes"]])
        self.assertEqual(
            ["bpy.types.Menu"],
            results["module_1"]["classes"][0]["base_classes"])
