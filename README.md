<div align=center>
  <h1>i3colors</h1>
  <img src=https://img.shields.io/badge/Language:-Python-yellow />
  <img src=https://img.shields.io/badge/WM:-i3wm-green />
  <img src=https://img.shields.io/badge/System:-GNU/Linux-blue />
</div>

A GUI tkinter program, intended to change the color of windows in i3wm. It also includes a togglable preview with how the finalized windows would look.

## Dependencies

This program depends on:
 - **Python** (tested version 3.12.4)
 - **Tk** and **tkinter** (on some distros has to be installed separately, how depends on distro)

To practically use this program, you will, of course, need **i3wm**. Its github is [here.](https://github.com/i3/i3)

## Instalation

Simply download the file and open it. If you want to be able to launch it in shell from anywhere, just put it into the `$PATH` or copy it over to `/usr/bin/` and if you wanna see it in menu like Rofi, just [create a desktop entry](https://www.baeldung.com/linux/desktop-entry-files).

## Usage

Using this program is very simple, if you know how to configure i3.

### File menu

In the **File** menu, you have three options (four but the last one is irrelevant).
 - **Open** will open a config file to edit - the default is in `$HOME/.config/i3/config`
 - **Write** will write config to a currently open file
 - **Backup** will create a backup of the file - in the same folder that the config file is in, it will create new files as following: `.file`,`..file` etc.

### Onscreen elements

On screen, you have:
 - **Editing** options menu, which will switch what mode of windows are you currently editing (in i3, you can set a different style based on if window is hovered over, if it's inactive.. ). The individual options (`border`,`background`..) are for changing the style itself.
 - **Undo** will set all the colors to the state in which they were when the file was initially loaded.
 - **Load backup** will load colors from a different config, but it will not start editing the config (mostly usedful for loading back backups, hence the name)
 - **Preview checkboxes** under the white canvas, in which you toggle a preview of different styles based on the criteria mentioned in **Editing**

## Screenshot

![image](https://github.com/user-attachments/assets/60c5c01a-3db3-4a3a-847e-1db861cb0d30)
