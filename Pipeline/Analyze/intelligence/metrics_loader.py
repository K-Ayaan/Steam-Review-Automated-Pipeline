import pandas as pd


class MetricsLoader:

    def load(self):

        try:

            return pd.read_csv(

                "outputs/campaign_metrics.csv"
            )

        except:

            return pd.DataFrame()
        