import whisper

from segment import dict_to_segment


def transcribe(fileName: str):
    model = whisper.load_model("large")
    result = model.transcribe(fileName)

    return [dict_to_segment(segment) for segment in result["segments"]]
