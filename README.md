# anki-tikz

Render TikZ diagrams in Anki using LuaLaTeX and Inkscape.

## Requirements

- Anki 23.10 or later (tested on 25.07.5)
- LuaLaTeX (TeX Live 2024+ or MiKTeX)
- Inkscape 1.0+

Install on macOS:
```bash
brew install --cask mactex inkscape
```

Install on Linux:
```bash
sudo apt-get install texlive-luatex inkscape
```

## Installation

1. Download the latest `.ankiaddon` file from releases
2. In Anki: Tools > Add-ons > Install from file
3. Restart Anki
4. Verify installation in Tools > Debug Console

Expected output:
```
LaTeX TikZ Inkscape: PATH updated to include Homebrew and TeX
LaTeX TikZ Inkscape: inkscape found at: /opt/homebrew/bin/inkscape
```

## Configuration

The addon uses LuaLaTeX to compile TikZ diagrams to PDF, then Inkscape to convert PDF to SVG.

Default pipeline:
```
LaTeX source → LuaLaTeX → PDF → Inkscape → SVG
```

Configure your note type's LaTeX preamble (Tools > Manage Note Types > Options):

```latex
\documentclass[12pt]{article}
\usepackage{tikz}
\usepackage{amsmath,amssymb}
\usetikzlibrary{arrows,positioning,calc}
\pagestyle{empty}
\begin{document}
```

## Usage

Use standard Anki LaTeX syntax with TikZ code:

```latex
[$$]
\begin{tikzpicture}
  \draw[->] (0,0) -- (2,0) node[right] {$x$};
  \draw[->] (0,0) -- (0,2) node[above] {$y$};
  \draw[thick,blue] (0,0) -- (1.5,1.5);
\end{tikzpicture}
[/$$]
```

Note: Replace `[$$]` and `[/$$]` with actual LaTeX delimiters (square brackets with dollar signs).

First render takes approximately 5-10 seconds. Subsequent displays are instant as images are cached.

## Configuration File

Advanced users can modify `config.json`:

```json
{
    "svgCommands": [
        ["lualatex", "-interaction=nonstopmode", "--shell-escape", "tmp.tex"],
        [
            "inkscape",
            "--pdf-poppler",
            "--export-text-to-path",
            "--export-plain-svg",
            "--export-area-drawing",
            "--export-filename=tmp.svg",
            "tmp.pdf"
        ]
    ]
}
```

To use XeLaTeX instead:
```json
{
    "svgCommands": [
        ["xelatex", "-interaction=nonstopmode", "--shell-escape", "tmp.tex"],
        ["inkscape", ...]
    ]
}
```

## Troubleshooting

### Inkscape not found

On macOS, if Inkscape is installed as an application:
```bash
sudo ln -s /Applications/Inkscape.app/Contents/MacOS/inkscape /usr/local/bin/inkscape
```

Or add to PATH in shell config:
```bash
export PATH="/Applications/Inkscape.app/Contents/MacOS:$PATH"
```

### LaTeX errors

Check the log file at:
- macOS/Linux: `/tmp/anki_temp/latex_log.txt`
- Windows: `%TEMP%\anki_temp\latex_log.txt`

Verify LaTeX installation:
```bash
lualatex --version
inkscape --version
```

### Missing TikZ libraries

Install additional packages:
```bash
sudo tlmgr install pgf tikz-cd circuitikz
```

## Technical Details

The addon overrides Anki's `latex.svgCommands` to use LuaLaTeX instead of the default latex engine. Inkscape converts the resulting PDF to SVG with:

- `--pdf-poppler`: Use Poppler for PDF rendering
- `--export-text-to-path`: Convert text to paths (eliminates font dependencies)
- `--export-plain-svg`: Generate clean SVG without metadata
- `--export-area-drawing`: Crop to content bounds

Generated SVG files are stored in Anki's media collection and sync across devices.

## Compatibility

- Anki 23.10+: Full support
- Anki 25.07.5: Tested and working
- AnkiMobile/AnkiDroid: Pre-rendered images sync and display correctly

The addon uses `gui_hooks.profile_did_open` to ensure proper initialization after Anki loads.

## Building

```bash
./build.sh
```

Produces `latex_svg_tikz_inkscape_v2.ankiaddon`.

## License

See LICENSE file.
