import argparse
from core import handle_single, handle_batch

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unified P2FA Tool (Adaptive Forced Alignment for EN & ZH)")
    
    # Global flags 
    parser.add_argument("-l", "--lang", choices=["en", "zh"], required=True, help="Audio language: en (English) or zh (Mandarin)")
    parser.add_argument("--save-seg", action="store_true", help="Keep intermediate segmented text files for Mandarin (default: off)")
    
    # Tier filter flags
    parser.add_argument("-np", "--no-phone", action="store_true", help="Remove the 'phone' tier from the output TextGrid")
    parser.add_argument("-nw", "--no-word", action="store_true", help="Remove the 'word' tier from the output TextGrid")
    
    subparsers = parser.add_subparsers(dest="mode", help="Run mode (single: single file, batch: batch processing)")
    subparsers.required = True

    # Single Mode
    parser_single = subparsers.add_parser("single", help="Process a single audio and transcript pair")
    parser_single.add_argument("wav", help="Input audio (.wav)")
    parser_single.add_argument("txt", help="Input transcript (.txt)")
    parser_single.add_argument("-o", "--output", dest="tg", required=True, help="Output file (.TextGrid)")
    parser_single.set_defaults(func=handle_single)

    # Batch Mode
    parser_batch = subparsers.add_parser("batch", help="Batch process a specified directory")
    parser_batch.add_argument("input_dir", help="Input directory containing wav and txt files")
    parser_batch.add_argument("-o", "--output", dest="output_dir", required=True, help="Output directory for TextGrids")
    parser_batch.add_argument("-r", "--recursive", action="store_true", help="Recursively process all subdirectories")
    parser_batch.set_defaults(func=handle_batch)

    args = parser.parse_args()
    args.func(args)