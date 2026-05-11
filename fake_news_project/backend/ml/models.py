from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier

def get_models(y_train=None):
    models = {
        'LogisticRegression': LogisticRegression(
            max_iter=2000,
            random_state=42,
            class_weight='balanced',
            C=1.5,
            solver='liblinear'
        ),

        'LinearSVM': LinearSVC(
            max_iter=3000,
            random_state=42,
            class_weight='balanced',
            C=1.0
        ),

        'RandomForest': RandomForestClassifier(
            n_estimators=300,
            max_depth=None,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            class_weight='balanced'
        ),

        'NaiveBayes': MultinomialNB(alpha=0.3),

        'KNN': KNeighborsClassifier(
            n_neighbors=5,
            weights='distance',
            metric='cosine'
        )
    }

    try:
        from xgboost import XGBClassifier

        if y_train is not None:
            scale_pos_weight = len(y_train[y_train == 0]) / len(y_train[y_train == 1])
        else:
            scale_pos_weight = 1

        models['XGBoost'] = XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
            eval_metric='logloss',
            n_jobs=-1,
            scale_pos_weight=scale_pos_weight
        )

        print("✅ XGBoost đã được thêm")
    except ImportError:
        print("⚠️ Không có XGBoost")

    return models