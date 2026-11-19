.. module:: bpy.path

.. function:: ensure_ext(filepath, ext, *, case_sensitive=False)

   Return the path with the extension added if it is not already set.

   :param filepath: The file path, a ``str`` or ``bytes``.
   :type filepath: _AnyStr
   :param ext: The extension to check for.
   :type ext: _AnyStr
   :param case_sensitive: Check for matching case when comparing extensions.
   :type case_sensitive: bool
   :return: The file path with the given extension, of the type of ``filepath``.
   :rtype: _AnyStr
