# Zork GUI

This repository contains a **GUI for the text-based game "Zork"**.

> ⚠️ **Important:** This project specifically requires **Frotz v2.54** (including dfrotz) to work properly.

## Installation

1. **Clone the Frotz repository:**

```bash
git clone https://gitlab.com/DavidGriffith/frotz.git
cd frotz
```

2. **Install required packages (Fedora example):**

```bash
sudo dnf install gtk3-devel glib2-devel libao-devel libmodplug-devel libsndfile-devel libvorbis-devel libsamplerate-devel
```

3. **Build and install Frotz (v2.54):**

```bash
make
sudo make install
```

4. **Build and install dfrotz (GUI version):**

```bash
make dfrotz
sudo make install-dfrotz
```

## Running the Game

After installation, you can start the Zork GUI by running:

```bash
python3 main.py
```

## Notes

- Ensure that your PATH includes `/usr/local/bin` if the installed binaries are not found.
- dfrotz provides a graphical interface, while `frotz` is the terminal version. Both can coexist.

