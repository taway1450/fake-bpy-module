.. mod-type:: new

.. module:: bpy.app.handlers

.. data:: _extension_repos_update_pre

   Private handlers for Blender's own handling of extension repositories (``addon_utils``, the
   Extensions add-on), left out of the API documentation.

   :type: list[collections.abc.Callable[..., None]]
   :mod-option: skip-refine

.. data:: _extension_repos_update_post

   :type: list[collections.abc.Callable[..., None]]
   :mod-option: skip-refine

.. data:: _extension_repos_sync

   :type: list[collections.abc.Callable[..., None]]
   :mod-option: skip-refine

.. data:: _extension_repos_files_clear

   :type: list[collections.abc.Callable[..., None]]
   :mod-option: skip-refine
