import subprocess
from pathlib import Path
from segmenter import DictSegmenter
from utils import filter_textgrid

def run_alignment(lang, wav_file, txt_file, tg_file, segmenter=None, save_seg=False, no_phone=False, no_word=False):
    """Underlying alignment routing."""
    actual_txt_to_use = str(txt_file)
    segmented_txt_path = None
    
    if lang == "en":
        script_path = Path("p2fa_en/align.py")
        cmd = ["python3", str(script_path), str(wav_file), actual_txt_to_use, str(tg_file)]
        
    elif lang == "zh":
        script_path = Path("p2fa_zh/Calign2textgrid.py")
        if segmenter is not None:
            # The intermediate _seg.txt file is also placed directly in the same directory as the flattened tg_file.
            segmented_txt_path = tg_file.with_name(f"{wav_file.stem}_seg.txt")
            segmenter.process_file(txt_file, segmented_txt_path)
            actual_txt_to_use = str(segmented_txt_path)
            
        cmd = ["python3", str(script_path), str(wav_file), actual_txt_to_use, str(tg_file)]
    else:
        raise ValueError("Unsupported language parameter")

    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        if tg_file.exists():
            filter_textgrid(tg_file, no_phone, no_word)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[Failed] Error processing file {wav_file.name}:\n{e.stderr}")
        return False
    finally:
        if segmented_txt_path and segmented_txt_path.exists() and not save_seg:
            segmented_txt_path.unlink()

def handle_single(args):
    """Handle single file mode"""
    print(f"[{args.lang.upper()}] Aligning single file: {args.wav} ...")
    segmenter = None
    if args.lang == "zh":
        segmenter = DictSegmenter(Path("p2fa_zh/model/dict"))
        
    tg_path = Path(args.tg)
    tg_path.parent.mkdir(parents=True, exist_ok=True)
    
    if run_alignment(args.lang, Path(args.wav), Path(args.txt), tg_path, segmenter, args.save_seg, args.no_phone, args.no_word):
        print("Alignment successful! TextGrid generated.")

def handle_batch(args):
    """Handle batch mode with optional recursive directory processing"""
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Apply recursive search if -r is passed
    if args.recursive:
        wav_files = list(input_dir.rglob("*.wav"))
    else:
        wav_files = list(input_dir.glob("*.wav"))

    if not wav_files:
        print(f"Error: No .wav files found in {input_dir}.")
        return

    segmenter = None
    if args.lang == "zh":
        print("Loading P2FA dictionary for NLP text segmentation...")
        segmenter = DictSegmenter(Path("p2fa_zh/model/dict"))

    print(f"Starting batch alignment, found {len(wav_files)} audio files, language: {args.lang.upper()}")
    success_count = 0
    failed_files = [] 

    for wav_file in wav_files:
        txt_file = wav_file.with_suffix(".txt")
        
        # Flat Output: Regardless of which subdirectory the original files are in, they are all generated directly under `output_dir`.
        tg_file = output_dir / f"{wav_file.stem}.TextGrid"

        if not txt_file.exists():
            print(f"[Skipped] Cannot find matching transcript: {txt_file.name}")
            failed_files.append(f"{wav_file.name} (missing transcript)")
            continue
            
        print(f"Processing: {wav_file.name} ...")
        if run_alignment(args.lang, wav_file, txt_file, tg_file, segmenter, args.save_seg, args.no_phone, args.no_word):
            success_count += 1
        else:
            failed_files.append(wav_file.name)

    print(f"\nBatch processing complete! Success: {success_count}/{len(wav_files)}")
    
    if failed_files:
        log_dir = Path(f"p2fa_{args.lang}/log")
        log_dir.mkdir(parents=True, exist_ok=True)
        error_log_path = log_dir / f"failed_log_{args.lang}.txt"
        
        with open(error_log_path, "w", encoding="utf-8") as f:
            f.write("\n".join(failed_files))
        print(f"Note: {len(failed_files)} files failed to align. The list has been written to -> {error_log_path}")