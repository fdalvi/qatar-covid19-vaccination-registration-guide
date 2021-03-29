#!/bin/bash

fonttools merge ../noto-sans/NotoSans-Light.ttf NotoSansTamil-Light.ttf
mv merged.ttf NotoSans_NotoSansTamil-Light.ttf
fonttools merge ../noto-sans/NotoSans-Bold.ttf NotoSansTamil-Bold.ttf
mv merged.ttf NotoSans_NotoSansTamil-Bold.ttf