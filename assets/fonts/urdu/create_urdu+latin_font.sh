#!/bin/bash

fonttools merge ../roboto-android/Roboto-Light.ttf NotoNaskhArabic-Regular.ttf
mv merged.ttf Roboto_NotoNaskhArabic-Regular.ttf
fonttools merge ../roboto-android/Roboto-Bold.ttf NotoNaskhArabic-Bold.ttf
mv merged.ttf Roboto_NotoNaskhArabic-Bold.ttf