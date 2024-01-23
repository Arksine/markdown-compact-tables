# Markdown Compact Tables

Extension for [Python Markdown](https://python-markdown.github.io/) allowing
for compact, readable Markdown tables. This extension is not a replacement
for the `tables` extension, but rather a supplement for it.

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

The built in tables extension will create new rows for each line.  This extension will
compact rows marked with a caret after the last pipe into the previous row. The
result of the above is a table with a single row.

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

This extension is inspired by the [cell_row_span](https://github.com/Neepawa/cell_row_span)
extension by Neepawa, who should be credited for the method of
using the table processor to detect the original blocks and
postprocessing the result.
