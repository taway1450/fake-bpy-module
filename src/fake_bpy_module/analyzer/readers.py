from docutils import nodes
from docutils.readers import standalone
from docutils.transforms import Transform, frontmatter, references

from fake_bpy_module.transformer.transformer_base import TransformerBase


class FileWideMetadataRemover(Transform):

    """Remove Sphinx's file-wide metadata (``:orphan:`` and the like).

    Sphinx reads a field list that comes before a page's title as metadata
    for the whole file. Left in place, it keeps docutils from promoting the
    title, so the ``module`` directive ends up inside a section and the page
    looks like it belongs to no module.
    """

    # Before DocTitle promotes the title.
    default_priority = frontmatter.DocTitle.default_priority - 1

    def apply(self) -> None:
        index = self.document.first_child_not_matching_class(
            nodes.PreBibliographic)
        if index is None:
            return
        if isinstance(self.document[index], nodes.field_list):
            del self.document[index]


class BpyRstDocsReader(standalone.Reader):
    def get_transforms(self) -> list[TransformerBase]:
        transforms = super().get_transforms()
        transforms.remove(references.DanglingReferences)
        transforms.append(FileWideMetadataRemover)

        return transforms
