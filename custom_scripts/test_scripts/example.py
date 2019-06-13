#!/usr/bin/env python
# -*- coding: utf-8 -*-

name = "test_1"
print name.replace("te", "foo")


import os
name, ext = os.path.splitext(fname)
os.rename(fname, name + '2007' + ext)

