from typing import Any
from dataclasses import dataclass
from app.config import get_settings

from app.logging.inference_log import log_inference
from app.logging.context_log import log_context_resolution  # ← added
import logging

settings = get_settings()
logger = logging.getLogger(__name__)


@dataclass
class ClassificationDecision:
    label: str
    confidence: float
    abstained: bool


def classify_document(text: str, context: Any) -> ClassificationDecision:
    """
    Applies:
    - Model prediction
    - Confidence threshold
    - Abstention logic
    - Logs inference and context usage
    """

    from app.classification.model import Classifier

    classifier = Classifier()
    if hasattr(context, "to_dict"):
        context_dict = context.to_dict()
    elif isinstance(context, dict):
        context_dict = context
    else:
        context_dict = {}

    logger.info("Classification request received", extra={"text": text[:100]})

    result = classifier.predict(text=text, context=context_dict)

    label = result.get("label")
    confidence = result.get("confidence", 0.0)

    abstained = False
    if settings.ENABLE_ABSTENTION and confidence < settings.CONFIDENCE_THRESHOLD:
        label = None
        abstained = True
        logger.warning(
            "Low confidence classification, abstaining", extra={"confidence": confidence}
        )

    # Log to persistent JSON files
    log_inference(
        label=label,
        confidence=confidence,
        abstained=abstained,
        text=text,
        context=context_dict,
    )

    # Minimal addition: log context usage
    log_context_resolution(context=context_dict, text=text)

    return ClassificationDecision(
        label=label,
        confidence=confidence,
        abstained=abstained,
    )
