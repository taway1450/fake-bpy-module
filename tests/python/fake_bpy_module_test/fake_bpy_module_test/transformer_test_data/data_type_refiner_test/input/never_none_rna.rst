.. module:: bpy.types

.. class:: bpy_struct

   .. data:: bl_rna

      The RNA type of this struct, a class attribute.

      :type: :class:`Struct`

.. class:: RenderViews

   .. attribute:: active

      Active Render View (never None)

      :type: :class:`SceneRenderView`

   .. attribute:: active_index

      Active index in render view array

      :type: int

.. class:: Object

   .. attribute:: active_material

      Active material being displayed

      :type: :class:`Material`

   .. attribute:: parent

      Parent object

      :type: :class:`Object`
