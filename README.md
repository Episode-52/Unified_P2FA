# Unified_P2FA

An adaptive, dual-language (English & Mandarin) Forced Alignment CLI tool based on P2FA. It features built-in NLP text segmentation, recursive batch processing, and precise TextGrid tier customization for phonetic and linguistic research.

## ✨ Core Features

* **Dual-Language Routing:** Seamlessly handles both English (original P2FA) and Mandarin acoustic models.
* **Intelligent NLP Segmentation (FMM):** Automatically applies Forward Maximum Matching based on the exact acoustic dictionary to segment Mandarin text (no whitespace required in transcripts), eliminating mismatch-induced OOV errors.
* **Recursive Batch Processing:** Scans complex directory trees and outputs aligned TextGrids into a flat, centralized directory.
* **Custom Tier Filtering:** Extract only the data you need by stripping out `phone` or `word` tiers directly from the generated TextGrid.
* **Clean OOV Logging:** Automatically aggregates Out-Of-Vocabulary words across batches into a centralized, deduplicated `MissingWords` log without cluttering the output directory.

## 🏗 Architecture

The project has been heavily modularized for maintainability and scale:

* `main.py` — The CLI entry point, handling argument parsing and mode selection.
* `core.py` — The alignment engine, managing subprocess routing, batch loops, and path resolution.
* `segmenter.py` — The NLP module, executing rule-based FMM segmentation and preserving special transcript tags (e.g., `{breath}`).
* `utils.py` — Post-processing utilities, including the robust TextGrid tier filter (`filter_textgrid`).

## ⚙️ Prerequisites & Installation

To run Unified_P2FA successfully, you must install **HTK (Hidden Markov Model Toolkit)** and several system-level audio processing libraries(Note: Based on testing, this project is only compatible with HTK 3.4)

### 1. Install System Libraries (sox, ffmpeg, python3)
The aligner relies on `sox` (and optionally `ffmpeg`) for downsampling and formatting audio on the fly. 

**For Ubuntu / Debian:**
```bash
sudo apt-get update
sudo apt-get install sox libsox-fmt-all ffmpeg python3 python3-pip build-essential gcc-multilib
```
**For macOS (using Homebrew):**
```bash
brew install sox ffmpeg python3
```
**For Arch Linux:**
```bash
sudo pacman -S sox ffmpeg python python-pip base-devel
```

### 2. Install HTK (Hidden Markov Model Toolkit)
You need to download the HTK source code from [http://htk.eng.cam.ac.uk](http://htk.eng.cam.ac.uk/). (Note: You may need to register a free account to download),if the official website is not accessible, you can visit [https://github.com/a8568730/HTK_HTS](https://github.com/a8568730/HTK_HTS) (use the `htk` branch for HTK 3.4, and the `hts` branch for HTK 3.4.1).

### 2.1 For Arch Linux
```bash
# Unzip HTK-3.4.tar.gz file in your current repository
tar -xvf HTK-3.4.tar.gz
cd htk

# Compile HTK
export CPPFLAGS=-UPHNALG
./configure --disable-hlmtools --disable-hslab
make clean    # necessary if you're not starting from scratch
make all
sudo make install # use "sudo" to make htk functions available for all users
```

### 2.2 For Ubuntu 22.04 / 24.04 LTS or later
```bash
# Assuming 64-bit platform, you may need 32-bit headers and libraries first
sudo apt-get install gcc-multilib
sudo chmod +x ./configure
./configure --disable-hlmtools --disable-hslab
make clean
make all
sudo make install

# Quick test if HVite works
HVite
```
### 2.3 For macOS (Apple Silicon / Intel)
(Tested on macOS Ventura 13.3.1 Apple M1 Max & macOS Sierra)
```bash
# Add CPPFLAGS, LIBRARY_PATH
export CPPFLAGS=-I/opt/X11/include
export LIBRARY_PATH=/opt/X11/lib

# If the above doesn't work, create a symlink:
sudo ln -s /opt/X11/include/X11 /usr/local/include/X11
```

## 🛠 Command Line Arguments

Unified_P2FA uses a mode-based CLI (`single` or `batch`) with global configurations.

### Global Options
| Argument | Description |
| :--- | :--- |
| `-l`, `--lang` | **[Required]** Target language: `en` (English) or `zh` (Mandarin). |
| `--save-seg` | *[Optional]* Keep intermediate NLP-segmented text files (`_seg.txt`). By default, they are silently deleted. |
| `-np`, `--no-phone` | *[Optional]* Remove the **phone** tier from the final TextGrid. |
| `-nw`, `--no-word` | *[Optional]* Remove the **word** tier from the final TextGrid. |

### Batch Mode Options (`batch`)
| Argument | Description |
| :--- | :--- |
| `input_dir` | **[Required]** The directory containing your `.wav` and `.txt` files. |
| `-o`, `--output` | **[Required]** The destination directory for flat TextGrid outputs. |
| `-r`, `--recursive`| *[Optional]* Recursively search all subdirectories within `input_dir`. |

### Single Mode Options (`single`)
| Argument | Description |
| :--- | :--- |
| `wav` | **[Required]** Path to the input `.wav` file. |
| `txt` | **[Required]** Path to the input `.txt` transcript. |
| `-o`, `--output` | **[Required]** Path and filename for the output `.TextGrid`. |


## 🚀 Usage 

### Command Syntax
The tool is executed via `main.py` with either the `single` or `batch` mode. You can combine global flags (`-np`, `-nw`, `--save-seg`) as needed.

### 1. Standard Batch Processing (Mandarin)
**Single Mode:**
```bash
python3 main.py -l [en|zh] [flags] single <audio.wav> <transcript.txt> -o <output.TextGrid>
```

**Batch Mode:**
```bash
python3 main.py -l [en|zh] [flags] batch <input_directory> [-r] -o <output_directory>
```
### Examples

**Standard Single Alignment (English as Example):**
```bash
python3 main.py -l en single p2fa_en/examples/ploppy.wav p2fa_en/examples/ploppy.txt -o output/ploppy.TextGrid
```

**Standard Batch Alignment (English and Mandarin):**
```bash
python3 main.py -l en batch p2fa_en/examples -o output
python3 main.py -l zh batch p2fa_zh/test -o output
```

**View Mandarin NLP Segmentation Results:**
If you want to additionally check the word segmentation results of the transcripts before Chinese alignment, you can add the --save-seg flag:
```bash
python3 main.py -l zh --save-seg batch p2fa_zh/test -o output
```

### 2. Recursive Batch with Tier Filtering (English)
If you want to customize the output data, you can strip out specific tiers directly from the generated TextGrid. You can use the `-np` flag to remove the `phone` tier, or the `-nw` flag to remove the `word` tier. For example, to align the English audio and drop the `word` tier (keeping only phones):
```bash
python3 main.py -l en -nw batch ./data -o ./results
```
### Examples
```bash
python3 main.py -l en -nw batch p2fa_en/examples -o output
```

## Acknowledgments and References

This project is built upon, combines, and heavily refactors the excellent work from the following original repositories. Sincere thanks to the original developers for their contributions to the open-source phonetics community:

* **[p2fa_py3](https://github.com/jaekookang/p2fa_py3)** developed by **Jaekoo Kang** (Core Python 3 port of the original Penn Phonetics Lab Forced Aligner).
* **[P2FA_Mandarin_py3](https://github.com/chenchenzi/P2FA_Mandarin_py3)** developed by **Chenzi Xu** and **Zhang Cong** (Mandarin acoustic models and script adaptation).
* **[Korean_FA](https://github.com/hyung8758/Korean_FA)** developed by **Hyungwon Yang** 
