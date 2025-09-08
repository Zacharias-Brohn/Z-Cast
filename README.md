# Z-Cast - Application Launcher for Wayland

Z-Cast is an application launcher designed specifically for Wayland compositors on Linux. Written in Python using [Fabric](https://github.com/Fabric-Development/fabric).

## Project Status

⚠️ **Early Development Stage** - This project is in its very early phases and may lack stability or complete feature implementation.

## Current Features

- CSS styling in `$HOME/.config/Z-Cast` (use GTK_DEBUG=interactive)
- Usage-based app list order

## Planned Features

- Fully customizable appearance
- Custom actions and commands

## Installation

Since Z-Cast uses Fabric you will need to install the following dependencies to run Fabric:
```bash
# Arch Linux
sudo pacman -S gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python python-pip python-gobject python-cairo python-loguru pkgconf

# OpenSUSE
sudo zypper install gtk3-devel cairo-devel gtk-layer-shell-devel libgirepository-1_0-1 libgirepository-2_0-0 gobject-introspection-devel python311 python311-pip python311-gobject python311-gobject-cairo python311-pycairo python311-loguru pkgconf

# Fedora
sudo dnf install gtk3-devel cairo-devel gtk-layer-shell-devel glib2 gobject-introspection-devel python3-devel python-pip python3-gobject python3-cairo python3-loguru pkgconf

```

It is recommended to use virtual environments (venv), such as `uv` or `conda`,
built-in python venv works as well.

```bash
# Clone the repository
git clone https://github.com/Zacharias-Brohn/z-cast.git
cd z-cast

# Create venv and activate
python3 -m venv venv/
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 main.py
```

## Inspiration
- [Spacerice](https://github.com/SlumberDemon/dotfiles)
- [Fabric](https://github.com/Fabric-Development/fabric)
