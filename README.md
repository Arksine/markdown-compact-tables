# Markdown Compact Tables

Extension for [Python Markdown](https://python-markdown.github.io/) allowing
for compact, readable Markdown tables. This extension is not a replacement
for the `tables` extension, but rather a supplement for it.  This is accomplished
by adding support for the following:

- Compacting multiple rows into a single row
- Defining attributes for the table, and optionally a caption
- Embedding elements in rows, including other tables

## Row Compacting

When attempting to create tables in Markdown, it is common to encounter
blocks like this:

```
| Header One | Header Two | Long Description |
|------------|------------|------------------|
| Cell One   | Cell Two   | I need to write a description here.  The description may be verbose.  I can use a table generator, however that is not useful if I need to review or modify the contents of the cell. Word wrap can help, but is still unnatural to read. |
```

This extension intends to resolve the above by compacting specified rows:

```
| Header One | Header Two | Long Description                                    |
|------------|------------|-----------------------------------------------------|
| Cell One   | Cell Two   | I need to write a description here. The description |
|            |            | may be verbose.  I can use a table generator,       |^
|            |            | however that is not useful if I need to review or   |^
|            |            | modify the contents of the cell. Word can help, but |^
|            |            | is still unnatural to read                          |^
```

The default behavior of Python Markdown's `tables`` extension will is to create
a new row for each line.  This extension will compact rows marked with a caret
after the last pipe into the previous row. The result of the above is a table
with a single row.

Another example:

```
| name   | breed    | description                    |
|--------|----------|--------------------------------|
| Tucker | Pug      | A mild mannered pup.           |
| Aria   | Labrador | She loves to play.  Constantly |
|        |          | begs for attention.            |^
| Yolo   | Shiba    | Aggressive.  Do not touch his  |
|        | Inu      | food bowl.  Stay away from his |^
|        |          | bed.                           |^
```

Yields a table like:
```
+--------+-----------+-------------------------------------------------------------------+
| name   | breed     | description                                                       |
+--------+-----------+-------------------------------------------------------------------+
| Tucker | Pug       | A mild mannered pup.                                              |
+--------+-----------+-------------------------------------------------------------------+
| Aria   | Labrador  | She loves to play. Constantly begs for attention.                 |
+--------+-----------+-------------------------------------------------------------------+
| Yolo   | Shiba Inu | Aggressive.  Do not touch his food bowl.  Stay away from his bed. |
+--------+-----------+-------------------------------------------------------------------+
```

The rendered output will wrap content in a cell based on the style.

If the `auto_insert_break` option is set to `true`, the `compact_tables` extension will
insert line breaks when joining each row.  The result will be like:

```
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
```

When rows are joined the location of empty cells does not impact the
result.  The following Markdown will all yield the same output:

```
| name   | breed    | description                    |
|--------|----------|--------------------------------|
| Yolo   | Shiba    | Aggressive.  Do not touch his  |
|        | Inu      | food bowl.  Stay away from his |^
|        |          | bed.                           |^

| name   | breed    | description                    |
|--------|----------|--------------------------------|
|        |          | Aggressive.  Do not touch his  |
| Yolo   | Shiba    | food bowl.  Stay away from his |^
|        | Inu      | bed.                           |^

| name   | breed    | description                    |
|--------|----------|--------------------------------|
|        | Shiba    | Aggressive.  Do not touch his  |
|        |          | food bowl.  Stay away from his |^
| Yolo   | Inu      | bed.                           |^
```

## Table Attributes

This extension allows for defining attributes on a table using a
method similar to Python Markdown's
[attr_list](https://python-markdown.github.io/extensions/attr_list/)
extension:

```
| name   | breed    | description                    |
|--------|----------|--------------------------------|
| Tucker | Pug      | A mild mannered pup.           |
| Aria   | Labrador | She loves to play.  Constantly |
|        |          | begs for attention.            |^
| Yolo   | Shiba    | Aggressive.  Do not touch his  |
|        | Inu      | food bowl.  Stay away from his |^
|        |          | bed.                           |^
{ #dog-desc .pets custom_attr="my custom" }
```

The above sets following attributes on the `<table>` element:
- `id="dog-desc"`
- `class="pets"`
- `custom_attr="my custom"`

Any text placed after the attributes will be the table's `<caption>`.
Note that at least one attribute must be defined to add a caption.
Pipes in the caption must be escaped, ie: `\|`.

Example:

```
| name   | breed    | description                    |
|--------|----------|--------------------------------|
| Tucker | Pug      | A mild mannered pup.           |
| Aria   | Labrador | She loves to play.  Constantly |
|        |          | begs for attention.            |^
| Yolo   | Shiba    | Aggressive.  Do not touch his  |
|        | Inu      | food bowl.  Stay away from his |^
|        |          | bed.                           |^
{ #dog-desc .pets } Dog Info
```

The result will be something like:

```
+----------------------------------------------------------------------------------------+
|                                        Dog Info                                        |
+--------+-----------+-------------------------------------------------------------------+
| name   | breed     | description                                                       |
+--------+-----------+-------------------------------------------------------------------+
| Tucker | Pug       | A mild mannered pup.                                              |
+--------+-----------+-------------------------------------------------------------------+
| Aria   | Labrador  | She loves to play. Constantly begs for attention.                 |
+--------+-----------+-------------------------------------------------------------------+
| Yolo   | Shiba Inu | Aggressive.  Do not touch his food bowl.  Stay away from his bed. |
+--------+-----------+-------------------------------------------------------------------+
```

## Embedding Elements

Its possible to embed an element with an id attribute in the table,
including other tables.  The element will take up a single cell
spanning all defined columns.  Rather than a caret, we use `+` to
define rows that will contain our embedded element, then specify
our desired item id in one of the cells in that row:

```
| name   | breed    | description                    |
|--------|----------|--------------------------------|
| Tucker | Pug      | A mild mannered pup.           |
|        |          | #tucker-schedule               |+
| Aria   | Labrador | She loves to play.  Constantly |
|        |          | begs for attention.            |^
| Yolo   | Shiba    | Aggressive.  Do not touch his  |
|        | Inu      | food bowl.  Stay away from his |^
|        |          | bed.                           |^
{ #dog-desc } Dog Info

| time     |     description    |
|----------|--------------------|
| 7:00 am  |  Breakfast         |
| 9:30 am  |  Walk to the park  |
| 12:15 pm |  Bath              |
| 5:00 pm  |  Dinner            |
{ #tucker-schedule }
```

Will result in something like:

```
+----------------------------------------------------------------------------------------+
|                                        Dog Info                                        |
+--------+-----------+-------------------------------------------------------------------+
| name   | breed     | description                                                       |
+--------+-----------+-------------------------------------------------------------------+
| Tucker | Pug       | A mild mannered pup.                                              |
+--------+-----------+-------------------------------------------------------------------+
|                            +----------+--------------------+                           |
|                            | time     |     description    |                           |
|                            +----------+--------------------+                           |
|                            | 7:00 am  |  Breakfast         |                           |
|                            +----------+--------------------+                           |
|                            | 9:30 am  |  Walk to the park  |                           |
|                            +----------+--------------------+                           |
|                            | 12:15 pm |  Bath              |                           |
|                            +----------+--------------------+                           |
|                            | 5:00 pm  |  Dinner            |                           |
|                            +----------+--------------------+                           |
+--------+-----------+-------------------------------------------------------------------+
| Aria   | Labrador  | She loves to play. Constantly begs for attention.                 |
+--------+-----------+-------------------------------------------------------------------+
| Yolo   | Shiba Inu | Aggressive.  Do not touch his food bowl.  Stay away from his bed. |
+--------+-----------+-------------------------------------------------------------------+
```

Each row identified as an embedded container is assigned a
`compact-container` attribute.  This can be used in javascript
and/or CSS to identify such rows, modify them, style them, etc.

Please note that embedded items are moved from their current
location in the element tree to the embedded cell.  The same
element cannot be embedded multiple times.  In addition, do not
attempt to embed an item that is a parent of the table.

## Credits

This extension is inspired by the [cell_row_span](https://github.com/Neepawa/cell_row_span)
extension by Neepawa, who should be credited for the method of
using the table processor to detect the original blocks and
postprocessing the result.
