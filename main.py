from pathlib import Path
import sys

import torch

from segment import segment_to_srt_block
from subtitle import add_srt_to_mp4
from transcribe import transcribe
from translate import create_chat_model, translate_texts_optimized


def main():
    file = sys.argv[1]

    input_path = Path(file)

    assert input_path.exists()
    assert input_path.suffix == ".mp4"

    parent_dir = input_path.parent

    input_file_path = str(input_path)
    srt_file_path = f"{parent_dir}/{input_path.stem}.srt"
    output_file_path = f"{parent_dir}/{input_path.stem} (sub).mp4"

    # 文字起こし
    print("Start transcribing...")
    segments = transcribe(input_file_path)
    print("Finish transcribe")

    # VRAMをクリア
    torch.cuda.empty_cache()

    # 翻訳
    print("Start translating...")

    llm = create_chat_model()

    english_texts = [segment.text for segment in segments]
    japanese_texts = translate_texts_optimized(llm, english_texts)

    for idx, segment in enumerate(segments):
        segment.text = japanese_texts[idx]

    transcript = "\n\n".join([segment_to_srt_block(segment) for segment in segments])

    # 字幕書き込み
    with open(srt_file_path, mode="w") as f:
        f.write(transcript)

    add_srt_to_mp4(input_file_path, srt_file_path, output_file_path)

    print(transcript)


if __name__ == "__main__":
    main()
