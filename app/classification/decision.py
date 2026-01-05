from dataclasses import dataclass
from app.config import get_settings

settings = get_settings()


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
    """

    from app.classification.model import Classifier

    classifier = Classifier()
    result = classifier.predict(text=text, context=context.to_dict())

    label = result.get("label")
    confidence = result.get("confidence", 0.0)

    abstained = False
    if settings.ENABLE_ABSTENTION and confidence < settings.CONFIDENCE_THRESHOLD:
        label = None
        abstained = True

    return ClassificationDecision(
        label=label,
        confidence=confidence,
        abstained=abstained,
    )
