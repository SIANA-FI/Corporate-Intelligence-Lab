class FinancialReader:

    def read(self, metrics):

        summary = []

        for metric, value in metrics.items():

            if value:

                summary.append(
                    f"{metric}: {value}"
                )

        return "\n".join(summary)