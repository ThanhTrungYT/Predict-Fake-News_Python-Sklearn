from sklearn.metrics import (
    classification_report,
    accuracy_score,
    f1_score,
    confusion_matrix
)
def evaluate_model(y_test, y_pred, name="Model"):
    print(f"\n{'='*60}")
    print(f"📊 Evaluation for {name}")
    print(f"{'='*60}")
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    print(f"{name} - Accuracy: {acc:.4f}")
    print(f"{name} - F1 Score (binary): {f1:.4f}")

    f1_macro = f1_score(y_test, y_pred, average='macro', zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average='weighted', zero_division=0)

    print(f"{name} - F1 Macro: {f1_macro:.4f}")
    print(f"{name} - F1 Weighted: {f1_weighted:.4f}")

    print("\n📄 Classification Report:")
    print(classification_report(
        y_test,
        y_pred,
        target_names=['Fake', 'Real'],
        digits=4,
        zero_division=0
    ))

    print("📊 Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    return acc, f1