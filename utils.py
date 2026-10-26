def filter_textgrid(tg_file, no_phone, no_word):
    """Parses and removes specific tiers from a TextGrid file."""
    if not no_phone and not no_word:
        return
    if no_phone and no_word:
        print("[Warning] Both -np and -nw are checked. The output TextGrid will be empty!")
        
    try:
        with open(tg_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        if 'ooTextFile short' not in lines[0]:
            print(f"[Warning] {tg_file.name} is not in standard short format. Skipping tier filter.")
            return

        header = lines[:6]
        original_num_tiers = int(lines[6].strip())
        
        tiers = []
        idx = 7
        for _ in range(original_num_tiers):
            tier_start = idx
            tier_name = lines[idx+1].strip().strip('"') 
            num_items = int(lines[idx+4].strip())
            tier_end = idx + 5 + (num_items * 3) 
            
            tiers.append({
                "name": tier_name,
                "lines": lines[tier_start:tier_end]
            })
            idx = tier_end
            
        filtered_tiers = []
        for t in tiers:
            if no_phone and t["name"] == "phone":
                continue
            if no_word and t["name"] == "word":
                continue
            filtered_tiers.append(t)
            
        with open(tg_file, 'w', encoding='utf-8') as f:
            f.writelines(header)
            f.write(f"{len(filtered_tiers)}\n")
            for t in filtered_tiers:
                f.writelines(t["lines"])
                
    except Exception as e:
        print(f"[Warning] Failed to filter TextGrid tiers for {tg_file.name}: {e}")