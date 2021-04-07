#!/bin/bash

fonttools merge ../noto-sans/NotoSans-Light.ttf NotoSansDevanagari-Light.ttf
mv merged.ttf NotoSans_NotoSansDevanagari-Light.ttf
fonttools merge ../noto-sans/NotoSans-Bold.ttf NotoSansDevanagari-Bold.ttf
mv merged.ttf NotoSans_NotoSansDevanagari-Bold.ttf