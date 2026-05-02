import io

import pandas as pd


class XlsxProcessor:
    def get_dataframes(self, content):

        stream = io.BytesIO(content)

        return pd.read_excel(stream, sheet_name=None, engine='openpyxl')

    def get_text(self, content):
        try:
            dfs = self.get_dataframes(content)
            full_text = ''

            for sheet_name, df in dfs.items():
                df = df.dropna(how='all').dropna(axis=1, how='all')
                if not df.empty:
                    full_text += f'--- Aba: {sheet_name} ---\n'
                    full_text += df.to_string(index=False, header=True) + '\n\n'

            return full_text
        except Exception as e:
            raise ValueError(f'Erro ao processar XLSX com Pandas: {str(e)}') from e
