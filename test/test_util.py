#!/usr/bin/env python

import configparser
import os
import unittest

from src.util import append_section, get_sections_only, load_template


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.fname = "themes/base16-3024.dunstrc"
        self.outconfig = "/tmp/example.ini"
        self.config = configparser.ConfigParser()

    def test_can_get_sections(self):
        _, self.config = get_sections_only(self.fname)

        self.assertEqual(3, len(self.config.sections()))
        self.assertListEqual(
            ["base16_low", "base16_normal", "base16_critical"], self.config.sections()
        )

    def test_can_append_section(self):
        self.config = append_section(self.fname)

        self.assertEqual(4, len(self.config.sections()))
        self.assertListEqual(
            ["base16_low", "base16_normal", "base16_critical", "general"],
            self.config.sections(),
        )

    def test_can_write_config(self):
        self.config = append_section(self.fname)

        with open(self.outconfig, "w") as configfile:
            self.config.write(configfile)

        self.assertTrue(os.path.isfile(self.outconfig))

        os.remove(self.outconfig)

    def test_can_load_template(self):
        template = load_template()

        self.assertListEqual(
            ["framecolor", "separatorcolor", "low", "normal", "critical"],
            list(template.blocks.keys()),
        )
