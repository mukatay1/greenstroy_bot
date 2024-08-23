from aiogram import Router, types

from utils.has_admin_privileges import check_admin_privileges

router = Router()


@router.message(lambda message: message.text == "Опоздавшие")
async def late_report_handler(message: types.Message) -> None:
    user_id = message.from_user.id
    error_message = check_admin_privileges(str(user_id))

    if error_message:
        await message.answer(error_message)
        return

    db: Session = SessionLocal()

    now = datetime.now()
    first_day_of_month = now.replace(day=1)
    last_day_of_month = (now.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    name_of_month_on_rus = months_russian[now.month]

    IGNORE_WORKERS = ['1195996440', '6468224924','133919486']
    employees = db.query(Employee).filter(not_(Employee.telegram_id.in_(IGNORE_WORKERS))).all()

        data = []
        for employee in employees:
            late_attendances = db.query(Attendance).filter(
                Attendance.employee_id == employee.id,
                Attendance.late == True,
                Attendance.date >= first_day_of_month,
                Attendance.date <= last_day_of_month
            ).all()

            late_days = [attendance.date for attendance in late_attendances]
            late_days_str = ', '.join([str(day) for day in late_days])

            data.append({
                "ФИО": employee.fio,
                "Телеграмм - ID": employee.telegram_id,
                "Телеграмм Ник": employee.full_name,
                "Количество опозданий": len(late_attendances),
                "Дни опозданий": late_days_str
            })

        df = pd.DataFrame(sorted(data, key=lambda x: x["Количество опозданий"], reverse=True))

        report_file = f"Отчет_по_опозданиям_за_{name_of_month_on_rus}.xlsx"
        df.to_excel(report_file, index=False, engine='openpyxl')

        wb = load_workbook(report_file)
        ws = wb.active
        ws.title = "Отчет"

        ws.insert_rows(1)
        ws.merge_cells('A1:E1')
        ws['A1'] = f'Отчет по опозданиям сотрудников за {name_of_month_on_rus}'
        ws['A1'].font = Font(size=16, bold=True)

        for column in ws.columns:
            max_length = 0
            column_letter = None
            for cell in column:
                if not isinstance(cell, MergedCell):
                    column_letter = cell.column_letter
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
            if column_letter:
                adjusted_width = (max_length + 2)
                ws.column_dimensions[column_letter].width = adjusted_width

        for row in ws.iter_rows(min_row=3, max_col=5):
            try:
                late_count = int(row[3].value)
            except (ValueError, TypeError):
                late_count = 0

            if late_count > 3:
                for cell in row:
                    cell.fill = red_fill
                    cell.border = black_border
            else:
                for cell in row:
                    cell.fill = green_fill
                    cell.border = black_border

        wb.save(report_file)

        report_document = FSInputFile(report_file)

        await message.answer_document(report_document,
                                      caption=f"Отчет по опозданиям сотрудников за {name_of_month_on_rus}")

        db.close()