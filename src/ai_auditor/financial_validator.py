class FinancialValidator:

    def _get_latest_value(self, metric):

        if not metric:
            return None

        if isinstance(metric, dict):

            try:
                latest_year = max(metric.keys())
                return float(metric[latest_year])
            except Exception:
                return None

        try:
            return float(metric)
        except Exception:
            return None

    def check_balance_sheet(
        self,
        assets,
        equity,
        liabilities
    ):

        assets_value = self._get_latest_value(assets)
        equity_value = self._get_latest_value(equity)
        liabilities_value = self._get_latest_value(liabilities)

        if not all([
            assets_value,
            equity_value,
            liabilities_value
        ]):
            return None

        difference = abs(
            assets_value - (
                equity_value + liabilities_value
            )
        )

        return difference

    def validate(self, metrics):

        warnings = []

        revenue = metrics.get("revenue")
        assets = metrics.get("assets")
        equity = metrics.get("equity")
        liabilities = metrics.get("liabilities")

        if not revenue:
            warnings.append(
                "Revenue not detected"
            )

        if not assets:
            warnings.append(
                "Assets not detected"
            )

        if not equity:
            warnings.append(
                "Equity not detected"
            )

        if not liabilities:
            warnings.append(
                "Liabilities not detected"
            )

        balance_difference = self.check_balance_sheet(
            assets,
            equity,
            liabilities
        )

        if balance_difference is not None:

            if balance_difference > 100:
                warnings.append(
                    f"Balance sheet mismatch: {balance_difference:.2f}"
                )

        return {
            "valid": len(warnings) == 0,
            "warnings": warnings,
            "balance_sheet_difference": balance_difference
        }