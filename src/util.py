#!/usr/bin/env python

import configparser
import os

from jinja2 import Template

N_UNCATEGORIZED = 3

title = '"Hello World"'
text = '"Have a nice day!"'


def _read_content(fname):
    with open(fname, "r") as fd:
        content = fd.read().splitlines(True)

    return content


def get_sections_only(fname):
    content = _read_content(fname)

    config = configparser.ConfigParser()
    config.read_string("".join(content[N_UNCATEGORIZED:]))

    return content[:N_UNCATEGORIZED], config


def append_section(fname):
    uncategorized, config = get_sections_only(fname)
    config.add_section("general")
    for i in range(N_UNCATEGORIZED - 1):  # 3rd line is a new line
        k, v = uncategorized[i].split("=")
        config["general"][k.strip()] = v.strip()

    return config


def load_template():
    with open("templates/dunstrc", "r") as fd:
        template = Template(fd.read())

    return template


def apply_theme(fname):
    config = append_section(fname)
    template = load_template()

    context = {}
    for section in config.sections():
        if section == "general":
            context["framecolor"] = config[section]["frame_color"]
            context["separatorcolor"] = config[section]["separator_color"]
        else:
            background = config[section]["background"]
            foreground = config[section]["foreground"]
            if section.endswith("low"):
                context["lowbackground"] = background
                context["lowforeground"] = foreground
            elif section.endswith("normal"):
                context["normalbackground"] = background
                context["normalforeground"] = foreground
            elif section.endswith("critical"):
                context["criticalbackground"] = background
                context["criticalforeground"] = foreground
            else:
                raise KeyError

    template.stream(context).dump(os.path.expanduser("~/.config/dunst/dunstrc"))


def run(theme, fname):
    cmd = "killall dunst;sleep 10;"
    cmd += "notify-send -u low {title} {text};"
    cmd += "notify-send -u normal {title} {text};"
    cmd += "notify-send -u critical {title} {text} | import -window Dunst {fname}"

    apply_theme(theme)
    os.system(cmd.format(title=title, text=text, fname=fname))
    # os.system("rm ~/.config/dunst/dunstrc")
