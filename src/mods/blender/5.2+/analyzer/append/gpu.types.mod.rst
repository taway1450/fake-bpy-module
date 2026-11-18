.. mod-type:: append

.. module:: gpu.types

.. class:: MatrixStackContext

   .. method:: __enter__()

      Entering it gives None, not the context.

      :rtype: None
      :mod-option rtype: skip-refine

   .. method:: __exit__(exc_type, exc_value, traceback)

      :type exc_type: type | None
      :mod-option arg exc_type: skip-refine
      :type exc_value: BaseException | None
      :mod-option arg exc_value: skip-refine
      :type traceback: BaseException | None
      :mod-option arg traceback: skip-refine
      :rtype: bool
      :mod-option rtype: skip-refine

.. class:: OffScreenStackContext

   .. method:: __enter__()

      Entering it gives None, not the context.

      :rtype: None
      :mod-option rtype: skip-refine

   .. method:: __exit__(exc_type, exc_value, traceback)

      :type exc_type: type | None
      :mod-option arg exc_type: skip-refine
      :type exc_value: BaseException | None
      :mod-option arg exc_value: skip-refine
      :type traceback: BaseException | None
      :mod-option arg traceback: skip-refine
      :rtype: bool
      :mod-option rtype: skip-refine
