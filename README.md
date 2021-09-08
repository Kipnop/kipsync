# Kipsync
A Python program to convert hand-authored midi pseudo-phonemes to midi tracks of viseme events compatible with OnyxToolKit (currently required).

There is no build executable, just download the two .py files and .yml file and run *python kipsync.py* in the same directory.

# System Requirements
- Python (2.x or 3.x, either should work fine)
- mido (*pip install mido*)
- yaml (*pip install pyyaml*)

# Commands
## pho2vis
The main (and currently only) functionality of Kipsync.  Run with *python kipsync.py pho2vis input.mid*, and the program will create a new midi file named *input_KIPSYNC.mid* in the same directory.  This resultant midi can be fed directly to OnyxToolKit, all midi tracks will be properly named.

The input midi needs the phonemes as text events on tracks named *PHONEMES_GEORGE*, *PHONEMES_JOHN*, etc.  All four members do not need phonemes for the program to work, it'll only output tracks for the phonemes it's given.

# Phonemes
Pre-set phonemes are listed in pho2vis-dict.yml, but feel free to add your own.  You can do so by creating a new entry in the file and adding the necessary visemes.

The phonemes are only containers for lists of visemes, and the way they blend together is not always the same.  Some sounds (like 'L' and 'N') only move the tongue by default, so other visemes like the lips will blend "over" these phonemes entirely, whereas the tongue position will be affected by them.  (This is a big reason for my inclusion of the "neut" phoneme for speech.)

You might notice that the "K" and "G" sounds lack phonemes: these sounds are created in the throat, and I've chosen to exclude them from the lipsync process: if one of these sounds is enunciated very clearly in your lipsync audio, I recommend faking it using the "neut" phoneme.

Final note: "neut" is for between phonemes, it isn't a non-speaking neutral expression.  For that, either use "none", or create your own.

# Eyebrow/Eye Shortcuts
The program currently has the following shorthands for eyes and eyebrows:
- brows_inner X (-255 thru 255)
- brows_outer X (-255 thru 255)
- lids X (0 thru 255)
- squint X (0 thru 255)
