from langchain_core.language_models import BaseChatModel
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL = "qwen3:14b"


def create_chat_model(model: str = MODEL, temperature: float = 0) -> BaseChatModel:
    """
    チャットモデルを作成する

    Args:
        model: 使用するLLMモデル
        temperature: 生成の温度（0に近いほど決定論的）

    Returns:
        日本語に翻訳されたテキストのリスト
    """

    llm = ChatOllama(model=model, temperature=temperature)
    return llm


def translate_texts_optimized(
    llm: BaseChatModel,
    texts: list[str],
    context_window: int = 3,
) -> list[str]:
    """
    英語のテキスト配列を日本語に翻訳（最適化版）

    Args:
        texts: 英語のテキストのリスト
        context_window: 前後何個のテキストを文脈として含めるか

    Returns:
        日本語に翻訳されたテキストのリスト
    """
    if not texts:
        return []

    translation_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """あなたは優秀な英日翻訳者です。
以下のルールに従って翻訳してください：
1. 前後の文脈を考慮した自然な日本語に翻訳
2. 文体や口調を統一
3. 固有名詞はそのまま残す
4. 翻訳結果のみを出力（説明不要）""",
            ),
            (
                "user",
                """
{context_info}

翻訳対象: {target_text}

上記の文脈を考慮して、「翻訳対象」を日本語に翻訳してください。
        """,
            ),
        ]
    )

    translation_chain = translation_prompt | llm | StrOutputParser()

    translated_texts = []

    for idx, text in enumerate(texts):
        try:
            # 文脈ウィンドウを計算
            start_idx = max(0, idx - context_window)
            end_idx = min(len(texts), idx + context_window + 1)

            # 文脈情報を構築
            context_parts = []

            # 前の文脈
            if idx > 0:
                previous_texts = texts[start_idx:idx]
                if previous_texts:
                    context_parts.append(f"前の文脈: {' '.join(previous_texts)}")

            # 後の文脈
            if idx < len(texts) - 1:
                next_texts = texts[idx + 1 : end_idx]
                if next_texts:
                    context_parts.append(f"後の文脈: {' '.join(next_texts)}")

            context_info = "\n".join(context_parts) if context_parts else "文脈なし"

            logger.info(f"翻訳中 ({idx + 1}/{len(texts)}): {text[:50]}...")

            # 翻訳実行
            translated = translation_chain.invoke(
                {"context_info": context_info, "target_text": text}
            )

            translated_texts.append(translated.strip())

        except Exception as e:
            logger.error(f"翻訳エラー (index {idx}): {e}")
            # エラー時はフォールバック
            translated_texts.append(f"[翻訳エラー: {text}]")

    return translated_texts
