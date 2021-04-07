#!/bin/bash

conda activate covid19-vaccination-guide

python build_guide.py --language en --output covid19-vaccine-registration-guide-qatar-english.pdf
python build_guide.py --language ur --output covid19-vaccine-registration-guide-qatar-urdu.pdf
python build_guide.py --language ta --output covid19-vaccine-registration-guide-qatar-tamil.pdf
python build_guide.py --language si --output covid19-vaccine-registration-guide-qatar-sinhala.pdf
python build_guide.py --language hi --output covid19-vaccine-registration-guide-qatar-hindi.pdf