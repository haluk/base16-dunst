#!/usr/bin/env python

# notify-send -u low $msgtitle $msgtext; notify-send -u normal $msgtitle $msgtext; notify-send -u critical $msgtitle $msgtext | import -window Dunst ss.png

import configparser

N_UNCATEGORIZED = 3


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
