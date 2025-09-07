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
