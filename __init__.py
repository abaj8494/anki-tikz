"""LaTeX SVG with TikZ - LuaLaTeX + Inkscape pipeline (PDF→SVG) - macOS Path Fix"""

import json
import os
from pathlib import Path
from aqt import mw, gui_hooks
import anki.latex


def apply_latex_config():
    """Apply LaTeX build configuration - called after profile opens"""
    # Fix PATH for macOS - add Homebrew paths
    # GUI apps don't inherit shell PATH, so we need to add common locations
    extra_paths = [
        "/opt/homebrew/bin",      # Apple Silicon Homebrew
        "/usr/local/bin",          # Intel Homebrew
        "/Library/TeX/texbin",     # MacTeX
        "/usr/texbin"              # Older MacTeX
    ]
    
    current_path = os.environ.get("PATH", "")
    for path in extra_paths:
        if path not in current_path and os.path.exists(path):
            current_path = f"{path}:{current_path}"
    
    os.environ["PATH"] = current_path
    print(f"LaTeX TikZ Inkscape: PATH updated to include Homebrew and TeX")
    
    # Load config
    config_path = Path(__file__).parent / "config.json"
    
    try:
        # Try to get user config from Anki's config system
        user_config = mw.addonManager.getConfig(__name__)
        if user_config:
            config = user_config
            print("LaTeX TikZ Inkscape: Using user config from Anki")
        else:
            # Load from default config.json
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("LaTeX TikZ Inkscape: Using default config.json")
    except Exception as e:
        print(f"LaTeX TikZ Inkscape: Error loading config: {e}")
        return
    
    # Override svgCommands if provided
    if "svgCommands" in config and config["svgCommands"]:
        anki.latex.svgCommands = config["svgCommands"]
        print(f"LaTeX TikZ Inkscape: ✓ svgCommands updated")
        print(f"LaTeX TikZ Inkscape:   LaTeX: {config['svgCommands'][0][0]}")
        print(f"LaTeX TikZ Inkscape:   Converter: {config['svgCommands'][1][0]}")
        
        # Verify inkscape is accessible
        import shutil
        inkscape_path = shutil.which("inkscape")
        if inkscape_path:
            print(f"LaTeX TikZ Inkscape:   ✓ inkscape found at: {inkscape_path}")
        else:
            print(f"LaTeX TikZ Inkscape:   ⚠️  WARNING: inkscape not found in PATH")
            print(f"LaTeX TikZ Inkscape:   Current PATH: {os.environ.get('PATH', '')}")
    
    # Override pngCommands if provided  
    if "pngCommands" in config and config["pngCommands"]:
        anki.latex.pngCommands = config["pngCommands"]
        print(f"LaTeX TikZ Inkscape: ✓ pngCommands updated")


# Hook into profile opening to ensure everything is initialized
gui_hooks.profile_did_open.append(apply_latex_config)

print("LaTeX TikZ Inkscape addon registered (LuaLaTeX → PDF → Inkscape → SVG)")

