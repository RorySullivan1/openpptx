# openpptx

Create, read, and modify PowerPoint .pptx files in pure Python.

## Overview

openpptx is a Python library for working with Microsoft PowerPoint presentations. It operates directly on the Office Open XML (OOXML) file format without requiring PowerPoint or any other software to be installed. Create presentations from scratch, open and modify existing ones, or merge slides across files — all with a clean, Pythonic API.

## Installation

```bash
pip install openpptx
```

Dependencies (installed automatically): lxml, Pillow, XlsxWriter, typing\_extensions.

## Quick Start

```python
from openpptx import Presentation
from openpptx.util import Inches, Pt

prs = Presentation()

# Add a title slide
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Hello, openpptx!"
slide.placeholders[1].text = "Automating PowerPoint with Python"

# Add a blank slide with a formatted text box
slide2 = prs.slides.add_slide(prs.slide_layouts[5])
txBox = slide2.shapes.add_textbox(Inches(1), Inches(1), Inches(8), Inches(2))
tf = txBox.text_frame
tf.text = "This was created programmatically."
p = tf.add_paragraph()
p.text = "Second paragraph with custom formatting."
p.font.size = Pt(24)
p.font.bold = True

prs.save("hello.pptx")
```

A presentation opened from a path (`Presentation("deck.pptx")`) leaves images and other binary
parts in that file until they are used, so a deck full of pictures opens without loading them
all into memory. Keep the file in place while you work on the presentation. Saving over it by
path (`prs.save("deck.pptx")`) is fine; opening it for writing yourself first empties it before
those parts can be read. A file-like object is read in full when it is opened.

Text can be found and replaced across the whole deck, even where PowerPoint has split a word
into several runs. The new text takes the formatting of the first run a match touches:

```python
prs = Presentation("deck.pptx")
prs.replace_text("ACME", "Acme Corp")  # slides, groups, tables and existing notes
for match in prs.find_text(r"Q[1-4] 20\d\d", regex=True):
    print(match.shape.name, match.paragraph.text)
```

## Features

- **Presentations** — create blank, open existing (`.pptx` / `.pptm` / `.potx`), save to file or stream, core + custom document properties, notes page size, slide-show settings (loop, kiosk/browse, pen color, slide range), custom shows, table-style listing, embedded fonts (list and remove)
- **Slides** — add, delete, duplicate, reorder, import across presentations, merge, computed slide numbers
- **180+ shape types** — autoshapes, pictures, tables, connectors, group shapes, freeforms, placeholders, OLE objects, movies, audio clips, callouts; 3D models, zooms and equations are listed read-only
- **Shape control** — z-order, visibility, lock aspect ratio, group containment, hyperlinks, click actions
- **Rich text formatting** — bold, italic, underline, color, size, shadow, strikethrough, caps, superscript/subscript, character spacing, kerning, bullets, tab stops, columns, RTL, vertical orientation
- **Find & replace** — across run boundaries, in a text frame, a slide or the whole deck (group members, table cells and notes included); literal or regex with `count`, keeping the formatting of the first run a match touches; run and character iteration, and merging runs split only by proofing state
- **Fill styles** — solid, gradient (linear, radial, rectangular, path), pattern, picture (stretched or tiled), background (no fill)
- **Line formatting** — width, color, dash styles, compound styles, cap and join styles, arrowheads, transparency, pattern fill
- **75+ chart types** — bar, line, pie, scatter, bubble, area, radar, stock, surface, doughnut, of-pie (plus 3D column, bar, line, pie and area variants, add and read); combo charts with trendlines, error bars, secondary axes, drop / hi-lo / up-down lines, log scale, 3D view, data labels with leader lines, data tables; Office 2016+ waterfall, histogram, box & whisker, treemap, sunburst and funnel charts (add and read; Pareto and region map read)
- **SmartArt** — detect SmartArt graphic frames, walk the node tree with text and levels, edit node text (PowerPoint re-lays out the diagram on open)
- **Tables** — create, insert/delete rows and columns, merge/split cells, borders (including diagonal), cell fills, cell text direction, banding, table styles
- **Visual effects** — outer/inner shadow with transparency, reflection, glow, soft edges
- **3D formatting** — extrusion, bevel, 3D scene, lighting, camera
- **Headers & footers** — per-slide date/time, footer text, slide-number overrides
- **Metadata** — slide and shape tags, sections, custom document properties
- **Comments** — add, read, delete with author tracking and positioning
- **Picture effects** — brightness, contrast, grayscale, transparency color
- **Theme access** — color schemes, font schemes, effect schemes, fill/line style lists; replace a master's theme from another deck or a `.thmx`
- **Master text styles** — per-level title/body/other formatting on slide masters, plus the presentation default text style
- **Bulk operations** — ShapeRange API for alignment, distribution, batch property setting
- **Accessibility** — alternative text, title, decorative flag on shapes

## Examples

See the [`examples/`](https://github.com/RorySullivan1/openpptx/tree/main/examples) directory for runnable scripts:

| Script | Description |
|--------|-------------|
| [`hello_world.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/hello_world.py) | Minimal presentation with title slide and core properties |
| [`add_textbox.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/add_textbox.py) | Text boxes with rich font formatting and paragraph alignment |
| [`add_picture.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/add_picture.py) | Insert and format images |
| [`picture_effects.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/picture_effects.py) | Brightness, contrast, grayscale, transparent colour, and cropping |
| [`shapes_and_fills.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/shapes_and_fills.py) | AutoShapes with solid, gradient, and pattern fills |
| [`shape_effects.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/shape_effects.py) | Shadow, glow, reflection, and 3D formatting |
| [`add_table.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/add_table.py) | Tables with merged cells, borders, and cell fills |
| [`add_chart.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/add_chart.py) | Bar and line charts with data labels and legends |
| [`add_chart_secondary_axis.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/add_chart_secondary_axis.py) | Combo chart: column plot plus a line plot on a secondary value axis |
| [`chart_3d_view.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/chart_3d_view.py) | 3D column, bar and pie charts; camera rotation, perspective and depth; floor and wall formatting |
| [`chart_trendlines_error_bars.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/chart_trendlines_error_bars.py) | Linear, polynomial and moving-average trendlines; fixed, percentage and std-dev error bars |
| [`batch_process.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/batch_process.py) | Process a folder of decks in parallel with a process pool (deck-wide `replace_text()`, per-file error reporting) |
| [`modern_charts.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/modern_charts.py) | Waterfall, histogram, box & whisker, treemap, sunburst and funnel charts, and a chart data table |
| [`slide_operations.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/slide_operations.py) | Duplicate, reorder, and delete slides |
| [`merge_presentations.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/merge_presentations.py) | Import and merge slides across presentations |
| [`bullet_lists.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/bullet_lists.py) | Bullet formatting, numbered lists, and indentation |
| [`connectors_and_groups.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/connectors_and_groups.py) | Connectors with arrowheads and group shapes |
| [`comments_and_metadata.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/comments_and_metadata.py) | Comments, slide and shape tags, sections, and custom properties |
| [`custom_slide_master_walk.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/custom_slide_master_walk.py) | Walk master → layout → slide placeholder inheritance, and override one |
| [`investor_presentation.py`](https://github.com/RorySullivan1/openpptx/blob/main/examples/investor_presentation.py) | A five-slide styled deck end to end |

## Requirements

- Python >= 3.9

## Limitations

- **Not a rendering engine** — cannot convert slides to images or PDF
- **Not a runtime** — cannot play slideshows or execute VBA macros
- **Not a print system** — cannot send presentations to a printer

## Stability

From 1.0.0, openpptx follows [Semantic Versioning](https://semver.org/). The public API is what the
[API reference](https://rorysullivan1.github.io/openpptx/) documents; `openpptx.oxml`, `openpptx.opc`
and `openpptx.parts` are internal. A deprecated name keeps working, with a `DeprecationWarning`,
until the next major release. The details are on the
[stability page](https://rorysullivan1.github.io/openpptx/stability.html).

## License

MIT. See [LICENSE](https://github.com/RorySullivan1/openpptx/blob/main/LICENSE).

openpptx is derived from [python-pptx](https://github.com/scanny/python-pptx) by Steve Canny,
also MIT, and LICENSE carries its notice as well. The two install side by side: python-pptx
imports as `pptx`, openpptx as `openpptx`.
