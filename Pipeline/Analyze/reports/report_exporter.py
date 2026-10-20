import pandas as pd


class ReportExporter:

    def export_developer_report(
        self,
        report,
        output_file
    ):

        df = pd.DataFrame(
            report
        )

        df.to_csv(

            output_file,

            index=False
        )

        print(
            f"Saved: {output_file}"
        )