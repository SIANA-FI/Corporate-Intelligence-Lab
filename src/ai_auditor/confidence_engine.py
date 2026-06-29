

class ConfidenceEngine:

    def calculate(
        self,
        metrics,
        statements_detected=True,
        table_detected=True
    ):

        results = {}

        for metric, value in metrics.items():

            confidence = 0

            if value not in [None, "", " "]:
                confidence += 40

            if statements_detected:
                confidence += 30

            if table_detected:
                confidence += 30

            confidence = min(confidence, 100)

            results[metric] = {
                "value": value,
                "confidence": confidence
            }

        return results