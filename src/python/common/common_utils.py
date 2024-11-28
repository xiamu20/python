import pandas as pd
from tabulate import tabulate  # pip install tabulate

def configure_dataframe_display(max_columns=None, max_rows=None, max_colwidth=None, display_width=None):
    """
    配置 Pandas 的显示选项，用于打印完整的 DataFrame 数据。

    参数:
        max_columns (int): 显示的最大列数（默认 None，显示所有列）。
        max_rows (int): 显示的最大行数（默认 None，显示所有行）。
        max_colwidth (int): 每列最大宽度（默认 None，无限制）。
        display_width (int): 显示的最大宽度（默认 None，根据屏幕动态调整）。
    """
    pd.set_option("display.max_columns", max_columns)  # 显示所有列
    pd.set_option("display.max_rows", max_rows)        # 显示所有行
    pd.set_option("display.max_colwidth", max_colwidth)  # 每列的宽度
    pd.set_option("display.width", display_width)      # 控制屏幕宽度

def print_dataframe(df, use_tabulate=True, tablefmt="grid"):
    """
    打印 Pandas DataFrame，以表格模式输出，支持完整显示。

    参数:
        df (pd.DataFrame): 要打印的 DataFrame 数据。
        use_tabulate (bool): 是否使用 tabulate 美观打印（默认 True）。
        tablefmt (str): 表格样式（仅在 use_tabulate=True 时生效）。
                        常用样式：'grid', 'plain', 'pipe', 'html' 等。
    """
    if use_tabulate:
        print(tabulate(df, headers="keys", tablefmt=tablefmt, showindex=True))
    else:
        # print(df)
        print(tabulate(df, headers='None', tablefmt='pretty', showindex=False))