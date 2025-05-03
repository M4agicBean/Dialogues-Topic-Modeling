import pandas as pd
import re
from bs4 import BeautifulSoup # type: ignore

def timestamps_preprocessing(input_file: str) -> pd.DataFrame:
    """
    Parses an SRT-like subtitle file, removes HTML tags, and extracts clean timestamped lines.

    Args:
        input_file (str): Path to the subtitle `.srt` or `.txt` file containing HTML-formatted lines.

    Returns:
        pd.DataFrame: A DataFrame with columns:
            - "Line": The dialogue text with formatting and extra characters removed.
            - "Strat Time": Start time of the subtitle block.
            - "End Time": End time of the subtitle block.
    """
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()
        
    soup = BeautifulSoup(content, "html.parser")
    content_no_html = soup.get_text()
    
    blocks = re.split(r'\n(?=\d+\n)', content_no_html.strip())
    data = {"Line": [], "Strat Time": [], "End Time": []}
    
    for block in blocks:
        lines = block.strip().split("\n")
        if len(lines) < 3:
            continue  # skip incomplete files
        
        time_line = lines[1]
        start = time_line.strip().split("-->")[0]
        end = time_line.strip().split("-->")[-1]
        
        # remove not important chars
        text = "".join(lines[2:]).strip().replace('"', "").replace("-", "")
        
        data["Line"].append(text)
        data["Strat Time"].append(start)
        data["End Time"].append(end)
    
    return pd.DataFrame(data)


def speakers_preprocessing(input_file: str) -> pd.DataFrame:
    """
    Parses a text file with speaker-labeled dialogue and returns a cleaned DataFrame.

    Each line in the input file should follow the format "Speaker: Line".
    The function removes bracketed text, cleans up punctuation, and normalizes spacing.

    Args:
        input_file (str): Path to the dialogue file.

    Returns:
        pd.DataFrame: A DataFrame with two columns:
            - "Speaker": The name of the speaker.
            - "Line": The cleaned dialogue line.
    """
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()

    data = {"Speaker": [], "Line": []}

    def remove_brackets(line: str) -> str:
        """Removes text within square or round brackets from a line."""
        text = re.sub(r"[\[\(]([^)\]]+)[\]\)]", "", line)
        return text.strip()
    
    lines = remove_brackets(content)
    
    for line in lines.split("\n"):
        if not line.strip():
            continue  # Skip empty lines
        
        line_splitted = line.split(":", 1)
        if len(line_splitted) != 2:
            continue  # Skip malformed lines
        
        speaker = line_splitted[0].strip()
        text = line_splitted[1].strip()

        # Remove quotes and normalize spaces
        text = text.replace('"', '').replace("'", "")
        text = " ".join(text.split())

        # Standardize punctuation and abbreviations
        text = re.sub(r"\.{3}([?!])", ".", text)     # ...! or ...? -> .
        text = re.sub(r"[?!]+", ".", text)           # !!! or ??? -> .
        text = re.sub(r"\.{2,}", ".", text)          # .. or ... -> .
        text = re.sub(r"\bDr\.", "Dr", text)
        text = re.sub(r"\ba\.m\.", "am", text)
        text = re.sub(r"\bMr\.", "Mr", text)
        
        data["Speaker"].append(speaker)
        data["Line"].append(text)
    
    return pd.DataFrame(data)

