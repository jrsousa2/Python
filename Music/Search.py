from Tags import compress, Remove_dupe_spaces


# Function to check if two strings have common words
def similar_ratio(base, comp, thres = 0.95):
    # Tokenize the strings into words (split on whitespace)
    base = compress(base.lower())
    base = Remove_dupe_spaces(base)
    comp = compress(comp.lower())
    comp = Remove_dupe_spaces(comp)
    words_base = base.split(" ")
    words_comp = comp.split(" ")

    # MAX SCORE
    base_len = len(base.replace(" ",""))
    comp_len = len(comp.replace(" ",""))
    max_len = max(base_len, comp_len)

    # Convert word lists to sets for faster intersection
    set1 = set(words_base)
    set2 = set(words_comp)

    # Check for common words using set intersection
    common_words = list(set1.intersection(set2))
    common_len = sum(len(word) for word in common_words)
    ratio = round(common_len / max_len, 5)

    Hit = ratio > thres
    
    # THESE METRICS BELOW ARE ALMOST ALL LENGTHS
    dict = {"base": base_len, "comp": comp_len, "common": common_len, "max": max_len, "ratio": ratio, "match": Hit}
    # If common_words is not empty, they have common words
    return dict