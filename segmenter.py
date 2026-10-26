class DictSegmenter:
    """NLP text segmenter based on the exact P2FA acoustic dictionary."""
    def __init__(self, dict_path):
        self.vocab = set()
        self.max_len = 1
        if dict_path.exists():
            with open(dict_path, 'r', encoding='utf-8') as f:
                for line in f:
                    parts = line.strip().split()
                    if parts:
                        word = parts[0]
                        self.vocab.add(word)
                        if len(word) > self.max_len:
                            self.max_len = len(word)
        else:
            print(f"[Warning] Dictionary not found at {dict_path}. FMM Segmentation might fail.")

    def segment_string(self, text):
        """Applies Forward Maximum Matching (FMM) against the loaded dictionary."""
        result = []
        i = 0
        n = len(text)
        while i < n:
            if text[i].isspace():
                i += 1
                continue
            
            if text[i] in ['{', '[', '<']:
                end_char = '}' if text[i] == '{' else (']' if text[i] == '[' else '>')
                end_idx = text.find(end_char, i)
                if end_idx != -1:
                    result.append(text[i:end_idx+1])
                    i = end_idx + 1
                    continue

            match_found = False
            for length in range(min(self.max_len, n - i), 0, -1):
                sub = text[i:i+length]
                if sub in self.vocab:
                    result.append(sub)
                    i += length
                    match_found = True
                    break
            
            if not match_found:
                result.append(text[i])
                i += 1
                
        return " ".join(result)

    def process_file(self, input_txt_path, output_txt_path):
        with open(input_txt_path, 'r', encoding='utf-8') as f:
            raw_text = f.read()
        
        segmented_text = self.segment_string(raw_text)
        
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(segmented_text)