import ffmpeg


def add_srt_to_mp4(video_file: str, srt_file: str, output_file: str, language="jpn"):
    """
    SRTファイルを自動的にmov_textに変換してMP4に追加
    """
    video_input = ffmpeg.input(video_file)
    subtitle_input = ffmpeg.input(srt_file)

    # -c:s mov_text が自動的にSRTからmov_textに変換します
    output = ffmpeg.output(
        video_input,
        subtitle_input,
        output_file,
        **{
            "c:v": "copy",  # 映像コーデックはコピー
            "c:a": "copy",  # 音声コーデックはコピー
            "c:s": "mov_text",  # 字幕をmov_text形式に変換
            "metadata:s:s:0": f"language={language}",
        },
    )

    ffmpeg.run(output, overwrite_output=True)
    print(f"字幕追加完了: {output_file}")
