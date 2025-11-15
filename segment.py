from dataclasses import dataclass


@dataclass
class Segment:
    id: int
    seek: int
    start: float
    end: float
    text: str
    tokens: list[int]
    temperature: float
    avg_logprob: float
    compression_ratio: float
    no_speech_prob: float


def dict_to_segment(segment) -> Segment:
    ret = Segment(
        id=segment["id"],
        seek=segment["seek"],
        start=segment["start"],
        end=segment["end"],
        text=segment["text"],
        tokens=segment["tokens"],
        temperature=segment["temperature"],
        avg_logprob=segment["avg_logprob"],
        compression_ratio=segment["compression_ratio"],
        no_speech_prob=segment["no_speech_prob"],
    )

    return ret


def format_timestamp(seconds: float):
    """秒をSRT形式のタイムスタンプに変換"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)

    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def segment_to_srt_block(segment: Segment):
    id = segment.id + 1
    start = format_timestamp(segment.start)
    end = format_timestamp(segment.end)
    text = segment.text.strip()

    return "\n".join([f"{id}", f"{start} --> {end}", text])
