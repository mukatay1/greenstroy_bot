from datetime import datetime, date


def parse_report_date(message_text: str) -> date:
    command_parts = message_text.split()
    if len(command_parts) > 1:
        date_str = command_parts[1]
        try:
            report_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Неверный формат даты. Используйте формат YYYY-MM-DD.")
    else:
        report_date = date.today()

    return report_date