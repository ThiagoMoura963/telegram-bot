import io

import pandas as pd


class CsvProcessor:
    def get_dataframe(self, content):

        stream = io.BytesIO(content)

        return pd.read_csv(stream)

    def get_text(self, content):

        try:
            df = self.get_dataframe(content)

            df = df.dropna(how='all')
            return df.to_string(index=False, header=True)
        except Exception as e:
            raise ValueError(f'Erro ao processar CSV com Pandas: {str(e)}') from e
