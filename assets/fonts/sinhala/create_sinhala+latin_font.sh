#!/bin/bash

fonttools merge ../noto-sans/NotoSans-Light.ttf NotoSansSinhala-Light.ttf
mv merged.ttf NotoSans_NotoSansSinhala-Light.ttf
fonttools merge ../noto-sans/NotoSans-Bold.ttf NotoSansSinhala-Bold.ttf
mv merged.ttf NotoSans_NotoSansSinhala-Bold.ttf