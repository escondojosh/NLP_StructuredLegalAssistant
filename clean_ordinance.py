from pathlib import Path
import re

# Put this script in the folder containing your ordinance TXT files.
INPUT_FOLDER = Path(__file__).parent
OUTPUT_FOLDER = INPUT_FOLDER / "cleaned_ordinances"


def clean_ordinance(text: str) -> str:
    # Normalize Windows/Linux line endings.
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove extra spaces at the start and end of each line.
    text = "\n".join(line.strip() for line in text.split("\n"))

    # Move joined ARTICLE / SECTION headings to a new line.
    heading_pattern = re.compile(
        r"(?i)(?<!\n)\s+(?=(?:ARTICLE\s+[IVXLCDM]+\b|"
        r"(?:SECTION|SEC\.?)\s*\d+\b))"
    )
    text = heading_pattern.sub("\n", text)

    # Remove trailing spaces and collapse repeated blank lines.
    text = "\n".join(line.rstrip() for line in text.split("\n"))
    text = re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", text)

    return text.strip() + "\n"


def main():
    OUTPUT_FOLDER.mkdir(exist_ok=True)

    txt_files = list(INPUT_FOLDER.glob("*.txt"))

    if not txt_files:
        print(f"No TXT files found in: {INPUT_FOLDER}")
        return

    for file_path in txt_files:
        try:
            original = file_path.read_text(encoding="utf-8-sig")
            cleaned = clean_ordinance(original)

            output_path = OUTPUT_FOLDER / f"{file_path.stem}-formatted.txt"
            output_path.write_text(cleaned, encoding="utf-8")
            print(f"Cleaned: {file_path.name} -> {output_path.name}")

        except UnicodeDecodeError:
            print(f"Skipped due to encoding issue: {file_path.name}")
        except OSError as error:
            print(f"Error processing {file_path.name}: {error}")

    print(f"\nFinished. Check this folder: {OUTPUT_FOLDER}")


if __name__ == "__main__":
    main()
