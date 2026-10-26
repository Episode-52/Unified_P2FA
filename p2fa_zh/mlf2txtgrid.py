#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# adapted from Jiahong Yuan by Chenzi Xu in Dec 2019
# Modified for Unified_P2FA pipeline

import codecs
import argparse
import os

def readAlignedMLF(mlffile, SR, wave_start):
    # This reads a MLF alignment output file with phone and word
    # alignments and returns a list of words, each word is a list containing
    # the word label followed by the phones, each phone is a tuple
    # (phone, start_time, end_time) with times in seconds.

    with codecs.open(mlffile, 'r', 'utf-8') as f:
        lines = [l.rstrip() for l in f.readlines()]

    if len(lines) < 3:
        raise ValueError("Alignment did not complete succesfully.")

    j = 2
    ret = []
    while (lines[j] != '.'):
        if (len(lines[j].split()) == 5):  # Is this the start of a word; do we have a word label?
            # Make a new word list in ret and put the word label at the beginning
            wrd = lines[j].split()[4]
            ret.append([wrd])

        # Append this phone to the latest word (sub-)list
        ph = lines[j].split()[2]
        if (SR == 11025):
            st = (float(lines[j].split()[0])/10000000.0 + 0.0125)*(11000.0/11025.0)
            en = (float(lines[j].split()[1])/10000000.0 + 0.0125)*(11000.0/11025.0)
        else:
            st = float(lines[j].split()[0])/10000000.0 + 0.0125
            en = float(lines[j].split()[1])/10000000.0 + 0.0125
        if st < en:
            ret[-1].append([ph, st+wave_start, en+wave_start])

        j += 1

    return ret


def writeTextGrid(outfile, word_alignments):
    # make the list of just phone alignments
    phons = []
    for wrd in word_alignments:
        phons.extend(wrd[1:])  # skip the word label

    # make the list of just word alignments
    # we're getting elements of the form:
    #   ["word label", ["phone1", start, end], ["phone2", start, end], ...]
    wrds = []
    for wrd in word_alignments:
        # If no phones make up this word, then it was an optional word
        # like a pause that wasn't actually realized.
        if len(wrd) == 1:
            continue
        # word label, first phone start time, last phone end time
        wrds.append([wrd[0], wrd[1][1], wrd[-1][2]])

    # write the phone interval tier using utf-8 to support Mandarin characters
    with codecs.open(outfile, 'w', 'utf-8') as fw:
        fw.write('File type = "ooTextFile short"\n')
        fw.write('"TextGrid"\n')
        fw.write('\n')
        fw.write(str(phons[0][1]) + '\n')
        fw.write(str(phons[-1][2]) + '\n')
        fw.write('<exists>\n')
        fw.write('2\n')
        fw.write('"IntervalTier"\n')
        fw.write('"phone"\n')
        fw.write(str(phons[0][1]) + '\n')
        fw.write(str(phons[-1][-1]) + '\n')
        fw.write(str(len(phons)) + '\n')
        for k in range(len(phons)):
            fw.write(str(phons[k][1]) + '\n')
            fw.write(str(phons[k][2]) + '\n')
            fw.write('"' + phons[k][0] + '"' + '\n')

        # write the word interval tier
        fw.write('"IntervalTier"\n')
        fw.write('"word"\n')
        fw.write(str(phons[0][1]) + '\n')
        fw.write(str(phons[-1][-1]) + '\n')
        fw.write(str(len(wrds)) + '\n')
        for k in range(len(wrds) - 1):
            fw.write(str(wrds[k][1]) + '\n')
            fw.write(str(wrds[k+1][1]) + '\n')
            fw.write('"' + wrds[k][0] + '"' + '\n')

        fw.write(str(wrds[-1][1]) + '\n')
        fw.write(str(phons[-1][2]) + '\n')
        fw.write('"' + wrds[-1][0] + '"' + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert an HTK MLF output file to a Praat TextGrid")
    parser.add_argument("mlf_file", help="Path to the input .mlf file")
    parser.add_argument("textgrid_file", nargs='?', help="Path to the output .TextGrid file (optional)")
    parser.add_argument("--sr", type=float, default=16000.0, help="Sampling rate used during alignment (default: 16000.0)")
    args = parser.parse_args()

    fname_in = args.mlf_file
    
    # Auto-generate output filename if not provided
    if args.textgrid_file:
        fname_out = args.textgrid_file
    else:
        fname_out = os.path.splitext(fname_in)[0] + ".TextGrid"

    wav_start = 0.0
    
    try:
        word_alignments = readAlignedMLF(fname_in, args.sr, wav_start)
        writeTextGrid(fname_out, word_alignments)
        print(f"[Success] Converted {fname_in} -> {fname_out}")
    except Exception as e:
        print(f"[Error] Failed to convert MLF: {e}")
