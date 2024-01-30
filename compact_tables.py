# Compact tables extension for Python Markdown
#
# Adds a post-process the Markdown Tables extension, joining marked
# rows
#
# Copyright (C) 2024 Eric Callahan <arksine.code@gmail.com>
#
# This file may be distributed under the terms of the BSD-3 license.
# https://opensource.org/license/bsd-3-clause
"""
Supports joining multiple table rows, resulting in table
Markdown that is compact and readable. For example:

| name   | breed    | description                    |
|--------|----------|--------------------------------|
| Tucker | Pug      | A mild mannered pup.           |
| Aria   | Labrador | She loves to play.  Constantly |
|        |          | begs for attention.            |^
| Yolo   | Shiba    | Aggressive.  Do not touch his  |
|        | Inu      | food bowl.  Stay away from his |^
|        |          | bed.                           |^

The standard table extension will create a table with six
rows from the above markdown.  When the compact_tables
extension is enabled the result will be a table with 3 rows.
The caret indicates that we want to join the current row
with the row above.  As you can see, its possible to join
as many rows as necessary.  The result will render something
like the following:

+--------+----------+--------------------------------+
| name   | breed    | description                    |
+--------+----------+--------------------------------+
| Tucker | Pug      | A mild mannered pup.           |
+--------+----------+--------------------------------+
| Aria   | Labrador | She loves to play.  Constantly |
|        |          | begs for attention.            |
+--------+----------+--------------------------------+
| Yolo   | Shiba    | Aggressive.  Do not touch his  |
|        | Inu      | food bowl.  Stay away from his |
|        |          | bed.                           |
+--------+----------+--------------------------------+

If line breaks are enabled the HTML will be rendered just as
shown above.  If they are not then the lines will be joined
with spaces.  Line breaks will be determined by the style, or
can be inserted by adding your own tags to the content.

"""
from __future__ import annotations
import re
from xml.etree.ElementTree import Element
from markdown.extensions import Extension, attr_list
from markdown.blockprocessors import BlockProcessor
from markdown.treeprocessors import Treeprocessor

from typing import TYPE_CHECKING, List, Optional

if TYPE_CHECKING:
    from markdown import Markdown
    from markdown.blockparser import BlockParser

TABLE_ATTR_RE = re.compile(r"\{(.+)\}(?: caption: (.+))?")

class Compactor(Treeprocessor):
    """
    Performs a post process on trees created by the "table" extension.
    Joins multiple rows together if a caret is found at the end of the
    row.  In addition, line breaks may be optionally inserted based on
    the configuration.
    """
    def __init__(self, ins_brk: bool) -> None:
        self.table_blocks: List[List[str]] = []
        self.sep = "<br/>" if ins_brk else " "
        super(Compactor, self).__init__()

    def add_block(self, block: str) -> None:
        """Called by the block processor when a table block is detected"""
        self.table_blocks.append(block.split("\n"))

    def run(self, root: Element) -> Optional[Element]:
        # Add table attributes first.  This will mutate each table
        # and apply the attributes before we come back around to
        # compact it.
        self.add_table_attributes(root)
        for tbl_index, table in enumerate(root.iter("table")):
            rows = self.table_blocks[tbl_index]
            if len(rows) < 4:
                # The top two rows are the header. If we have a table
                # with a single row there is nothing to do.
                continue
            rows = rows[2:]
            tbody = table.find("tbody")
            if tbody is None:
                continue
            assert len(rows) == len(tbody)
            row_remove: List[Element] = []  # List of tr elements to remove
            prev_tr: Optional[Element] = None
            for orig_row, tr in zip(rows, tbody):
                if prev_tr is None:
                    # Can't join first row, so skip it and initialize
                    # the previous tr element
                    prev_tr = tr
                    continue
                if orig_row.strip().endswith("|^"):
                    # join current tds with previous tds
                    for prev_td, cur_td in zip(prev_tr, tr):
                        if not cur_td.text:
                            continue
                        if not prev_td.text:
                            prev_td.text = cur_td.text
                        else:
                            prev_td.text += self.sep + cur_td.text
                    row_remove.append(tr)
                else:
                    prev_tr = tr

            # Remove joined tr elements
            for tr in row_remove:
                tbody.remove(tr)

        return None

    def add_table_attributes(self, root: Element) -> None:
        """
        Iterates through all tables and applies attributes specified
        in the last row.
        """
        for tbl_index, table in enumerate(root.iter("table")):
            rows = self.table_blocks[tbl_index]
            if len(rows) < 4:
                # The top two rows are the header. If we have a table
                # with a single row there is nothing to do.
                continue
            tbody = table.find("tbody")
            if tbody is None:
                continue
            attr_match = TABLE_ATTR_RE.match(rows[-1])
            caption: Optional[str] = None
            if attr_match is not None:
                attrs = attr_match.group(1)
                caption = attr_match.group(2)
                rows.pop()
                tbody.remove(tbody[-1])
                if attrs:
                    self.assign_attrs(table, attrs)
                # Insert Caption If Found
                if caption is not None:
                    captag = Element("caption")
                    captag.text = caption.strip()
                    table.insert(0, captag)

    def assign_attrs(self, elem: Element, attrs: str) -> None:
        """ Assign `attrs` to element. Code from attr_list extension."""
        for k, v in attr_list.get_attrs(attrs):
            if k == '.':
                # add to class
                cls = elem.get('class')
                if cls:
                    elem.set('class', '{} {}'.format(cls, v))
                else:
                    elem.set('class', v)
            else:
                # assign attribute `k` with `v`
                elem.set(self.sanitize_name(k), v)

    def sanitize_name(self, name: str) -> str:
        """
        Sanitize name as 'an XML Name, minus the ":"'.
        See https://www.w3.org/TR/REC-xml-names/#NT-NCName

        Code from attr_list extension.
        """
        return attr_list.AttrListTreeprocessor.NAME_RE.sub('_', name)

class TableBlockRetreiver(BlockProcessor):
    """
    Retreives the orignal blocks detected by the "table" extension.
    The ReadableTableProcessor will use these blocks to find the
    marker (a caret) at the of each row.
    """

    def __init__(
        self,
        compactor: Compactor,
        md_parser: BlockParser
    ) -> None:
        self.compactor = compactor
        self.orig_table_procesor = md_parser.blockprocessors['table']
        super(TableBlockRetreiver, self).__init__(md_parser)

    def test(self, parent: Element, block: str):
        """Use the table procesor to test if this block is a valid table"""
        return self.orig_table_procesor.test(parent, block)

    def run(self, parent: Element, blocks: List[str]):
        """Add the block to the compactor"""
        self.compactor.add_block(blocks[0])
        return False

class CompactTableExtension(Extension):
    """ Allows the Markdown Table source to be compact and readable """

    def __init__(self, **kwargs):
        self.config = {
            "auto_insert_break": [False, "True to enable automatic break insertion"],
        }
        super().__init__(**kwargs)
    def extendMarkdown(self, md: Markdown) -> None:
        ins_brk = self.getConfig("auto_insert_break", True)
        if 'table' in md.parser.blockprocessors:
            compactor = Compactor(ins_brk)
            md.parser.blockprocessors.register(
                TableBlockRetreiver(compactor, md.parser),
                "compact_tables", 80
            )
            md.treeprocessors.register(compactor, "compact_tables", 30)

def makeExtension(*args, **kwargs):
    return CompactTableExtension(*args, **kwargs)
