from config import black_border


def apply_border(ws, num_columns):
    for row in ws.iter_rows(min_row=1, min_col=1, max_col=num_columns):
        for cell in row:
            cell.border = black_border
