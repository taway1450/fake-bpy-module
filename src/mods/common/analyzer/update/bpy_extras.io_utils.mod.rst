.. mod-type:: update

.. module:: bpy_extras.io_utils

.. function:: orientation_helper(axis_forward, axis_up)

   :generic-types: _GenericType1
   :rtype: collections.abc.Callable[[_GenericType1], _GenericType1]
   :mod-option rtype: skip-refine

.. class:: ExportHelper

   .. attribute:: filepath

      :type: typing.Annotated[str, bpy.props.StringProperty(name="File Path", description="Filepath used for exporting the file", maxlen=1024, subtype="FILE_PATH")]
      :mod-option: skip-refine

   .. attribute:: check_existing

      :type: typing.Annotated[bool, bpy.props.BoolProperty(name="Check Existing", description="Check and warn on overwriting existing files", default=True, options={"HIDDEN"})]
      :mod-option: skip-refine

   .. method:: invoke(context, event)

      :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

.. class:: ImportHelper

   .. attribute:: filepath

      :type: typing.Annotated[str, bpy.props.StringProperty(name="File Path", description="Filepath used for importing the file", maxlen=1024, subtype="FILE_PATH", options={"SKIP_PRESET", "HIDDEN"})]
      :mod-option: skip-refine

   .. method:: invoke(context, event)

      :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]

   .. method:: invoke_popup(context, confirm_text)

      :rtype: set[Literal[:ref:`rna_enum_operator_return_items`]]
