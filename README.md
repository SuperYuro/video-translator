# Video Translator

英語動画から[Whisper](https://github.com/openai/whisper)で文字起こしを行い、LLMで日本語に翻訳してffmpegで字幕を付けた動画を生成します

## 必要なもの

- [uv](https://docs.astral.sh/uv/)
- Ollama
    - デフォルトでは`qwen3:14b`を使います
- ffmpeg

## あったほうがいいもの

- NVIDIAのGPU
    - VRAMが12GB以上あると安心です

## 使い方

動画ファイルへのパスを引数にして`main.py`を実行すると、動画ファイルと同じ場所に`{動画ファイル名} (sub).mp4`が生成されます。

> [!CAUTION]
> - 複数ファイルは対応していません（今後対応予定）
> - mp4形式のファイルのみ対応しています

```console
$ uv run main.py {動画ファイルへのパス}
```

