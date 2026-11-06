.. module:: bpy.app.handlers

.. data:: load_post

   on loading a new blend file (after).

   :type: list[Callable[[str], None]]

.. data:: persistent

   Function decorator for callback functions not to be removed when loading new files

   :type: type
