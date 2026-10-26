# Unified_P2FA

An adaptive, dual-language (English & Mandarin) Forced Alignment CLI tool based on P2FA. It features built-in NLP text segmentation, recursive batch processing, and precise TextGrid tier customization for phonetic and linguistic research.

## ✨ Core Features

* **Dual-Language Routing:** Seamlessly handles both English (original P2FA) and Mandarin acoustic models.
* **Intelligent NLP Segmentation (FMM):** Automatically applies Forward Maximum Matching based on the exact acoustic dictionary to segment Mandarin text (no whitespace required in transcripts), eliminating mismatch-induced OOV errors.
* **Recursive Batch Processing:** Scans complex directory trees and outputs aligned TextGrids into a flat, centralized directory.
* **Custom Tier Filtering:** Extract only the data you need by stripping out `phone` or `word` tiers directly from the generated TextGrid.
* **Clean OOV Logging:** Automatically aggregates Out-Of-Vocabulary words across batches into a centralized, deduplicated `MissingWords` log without cluttering the output directory.

---

## 🏗 Architecture

The project has been heavily modularized for maintainability and scale:

* `main.py` — The CLI entry point, handling argument parsing and mode selection.
* `core.py` — The alignment engine, managing subprocess routing, batch loops, and path resolution.
* `segmenter.py` — The NLP module, executing rule-based FMM segmentation and preserving special transcript tags (e.g., `{breath}`).
* `utils.py` — Post-processing utilities, including the robust TextGrid tier filter (`filter_textgrid`).

---

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

---

## 🚀 Usage Examples

### 1. Standard Batch Processing (Mandarin)
Process all audio-transcript pairs in `p2fa_zh/test` and export TextGrids to the `output` folder:
```bash
python3 main.py -l zh batch p2fa_zh/test -o output
```
### 2. Recursive Batch with Tier Filtering (English)
Search through all subfolders in `./data`, align the English audio, drop the `phone` tier (keeping only words), and output everything flatly into `./results`:
```bash
python3 main.py -l en -np batch ./data -r -o ./results
```
---

## Acknowledgments

This project is built upon, combines, and heavily refactors the excellent work from the following original repositories. Sincere thanks to the original developers for their contributions to the open-source phonetics community:

* **[p2fa_py3](https://github.com/jaekookang/p2fa_py3)** developed by **Jaekoo Kang** (Core Python 3 port of the original Penn Phonetics Lab Forced Aligner).
* **[P2FA_Mandarin_py3](https://github.com/chenchenzi/P2FA_Mandarin_py3)** developed by **Chenzi Xu** (Mandarin acoustic models and script adaptation).
