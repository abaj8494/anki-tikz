# LaTeX TikZ with Inkscape - macOS Path Fixed

This version fixes the PATH issue on macOS where Anki can't find Inkscape.

## What Was Fixed

macOS GUI apps (like Anki) don't inherit the shell's PATH. Even though `which inkscape` works in Terminal, Anki couldn't find it.

This version adds `/opt/homebrew/bin` and other common paths to the environment before running LaTeX commands.

## Installation

1. **Uninstall previous version**:
   - Tools > Add-ons
   - Delete "LaTeX TikZ Inkscape"
   - Restart Anki

2. **Install this version**:
   - Tools > Add-ons > Install from file...
   - Select `latex_svg_tikz_inkscape_v2.ankiaddon`
   - Restart Anki

3. **Verify**:
   - Tools > Debug Console
   - Look for:
     ```
     LaTeX TikZ Inkscape: PATH updated to include Homebrew and TeX
     LaTeX TikZ Inkscape: ✓ inkscape found at: /opt/homebrew/bin/inkscape
     ```

## Test It

Create a card with:

```latex
[$$]
\begin{tikzpicture}
  \draw[->] (0,0) -- (2,0) node[right] {$x$};
  \draw[->] (0,0) -- (0,2) node[above] {$y$};
  \draw[thick,blue] (0,0) -- (1.5,1.5);
\end{tikzpicture}
[/$$]
```

Should render perfectly now!

## The Pipeline

1. **LuaLaTeX → PDF**: `lualatex tmp.tex` → `tmp.pdf` ✅ (This was working)
2. **Inkscape → SVG**: `inkscape tmp.pdf` → `tmp.svg` ✅ (Now will work)

## Configuration

Same as before - your Emacs-style pipeline:

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

Your preamble (Tools > Manage Note Types > Options):
```latex
\usepackage{tikz}
\usetikzlibrary{arrows,positioning,calc}
```

