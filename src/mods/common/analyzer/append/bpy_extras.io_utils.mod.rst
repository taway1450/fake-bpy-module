.. mod-type:: append

.. module:: bpy_extras.io_utils

.. class:: ExportHelper

   .. attribute:: filepath

      :type: typing.Annotated[str, bpy.props.StringProperty(name="File Path", description="Filepath used for exporting the file", maxlen=1024, subtype="FILE_PATH")]
      :mod-option: skip-refine

   .. attribute:: check_existing

      :type: typing.Annotated[bool, bpy.props.BoolProperty(name="Check Existing", description="Check and warn on overwriting existing files", default=True, options={"HIDDEN"})]
      :mod-option: skip-refine

.. class:: ImportHelper

   .. attribute:: filepath

      :type: typing.Annotated[str, bpy.props.StringProperty(name="File Path", description="Filepath used for importing the file", maxlen=1024, subtype="FILE_PATH", options={"SKIP_PRESET", "HIDDEN"})]
      :mod-option: skip-refine
