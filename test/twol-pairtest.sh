#!/bin/bash

cat test/ky-verbs.pairtest | hfst-pair-test .deps/kir.twol.hfst

exit 0
