.. mod-type:: update

.. module:: bpy.app.handlers

.. data:: animation_playback_post

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`, :class:`bpy.types.Depsgraph`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`], None]]
   :mod-option: skip-refine

.. data:: animation_playback_pre

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`, :class:`bpy.types.Depsgraph`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`], None]]
   :mod-option: skip-refine

.. data:: blend_import_post

   :type: list[collections.abc.Callable[[:class:`bpy.types.BlendImportContext`], None] | collections.abc.Callable[[:class:`bpy.types.BlendImportContext`, None], None]]
   :mod-option: skip-refine

.. data:: blend_import_pre

   :type: list[collections.abc.Callable[[:class:`bpy.types.BlendImportContext`], None] | collections.abc.Callable[[:class:`bpy.types.BlendImportContext`, None], None]]
   :mod-option: skip-refine

.. data:: composite_cancel

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: composite_post

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: composite_pre

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: depsgraph_update_post

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`, :class:`bpy.types.Depsgraph`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`], None]]
   :mod-option: skip-refine

.. data:: depsgraph_update_pre

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: exit_pre

   :type: list[collections.abc.Callable[[bool], None] | collections.abc.Callable[[bool, None], None]]
   :mod-option: skip-refine

.. data:: frame_change_post

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`, :class:`bpy.types.Depsgraph`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`], None]]
   :mod-option: skip-refine

.. data:: frame_change_pre

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: load_factory_preferences_post

   :type: list[collections.abc.Callable[[None], None] | collections.abc.Callable[[None, None], None]]
   :mod-option: skip-refine

.. data:: load_factory_startup_post

   :type: list[collections.abc.Callable[[None], None] | collections.abc.Callable[[None, None], None]]
   :mod-option: skip-refine

.. data:: load_post

   :type: list[collections.abc.Callable[[str], None] | collections.abc.Callable[[str, None], None]]
   :mod-option: skip-refine

.. data:: load_post_fail

   :type: list[collections.abc.Callable[[str], None] | collections.abc.Callable[[str, None], None]]
   :mod-option: skip-refine

.. data:: load_pre

   :type: list[collections.abc.Callable[[str], None] | collections.abc.Callable[[str, None], None]]
   :mod-option: skip-refine

.. data:: object_bake_cancel

   :type: list[collections.abc.Callable[[:class:`bpy.types.Object`], None] | collections.abc.Callable[[:class:`bpy.types.Object`, None], None]]
   :mod-option: skip-refine

.. data:: object_bake_complete

   :type: list[collections.abc.Callable[[:class:`bpy.types.Object`], None] | collections.abc.Callable[[:class:`bpy.types.Object`, None], None]]
   :mod-option: skip-refine

.. data:: object_bake_pre

   :type: list[collections.abc.Callable[[:class:`bpy.types.Object`], None] | collections.abc.Callable[[:class:`bpy.types.Object`, None], None]]
   :mod-option: skip-refine

.. data:: redo_post

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: redo_pre

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: render_cancel

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: render_complete

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: render_init

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: render_post

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: render_pre

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: render_stats

   :type: list[collections.abc.Callable[[str], None] | collections.abc.Callable[[str, None], None]]
   :mod-option: skip-refine

.. data:: render_write

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: save_post

   :type: list[collections.abc.Callable[[str], None] | collections.abc.Callable[[str, None], None]]
   :mod-option: skip-refine

.. data:: save_post_fail

   :type: list[collections.abc.Callable[[str], None] | collections.abc.Callable[[str, None], None]]
   :mod-option: skip-refine

.. data:: save_pre

   :type: list[collections.abc.Callable[[str], None] | collections.abc.Callable[[str, None], None]]
   :mod-option: skip-refine

.. data:: translation_update_post

   :type: list[collections.abc.Callable[[None], None] | collections.abc.Callable[[None, None], None]]
   :mod-option: skip-refine

.. data:: undo_post

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: undo_pre

   :type: list[collections.abc.Callable[[:class:`bpy.types.Scene`], None] | collections.abc.Callable[[:class:`bpy.types.Scene`, None], None]]
   :mod-option: skip-refine

.. data:: version_update

   :type: list[collections.abc.Callable[[None], None] | collections.abc.Callable[[None, None], None]]
   :mod-option: skip-refine

.. data:: xr_session_start_pre

   :type: list[collections.abc.Callable[[None], None] | collections.abc.Callable[[None, None], None]]
   :mod-option: skip-refine
