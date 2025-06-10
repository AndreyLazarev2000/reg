import csv
import re
from pprint import pprint


def process_contacts(contacts_list):
    # Шаг 1: Обработка ФИО
    processed_contacts = []
    for contact in contacts_list:
        # Собираем первые три элемента (ФИО)
        fio = ' '.join(contact[:3]).split()
        # Дополняем до 3 элементов (если отчество отсутствует)
        fio += [''] * (3 - len(fio))
        lastname, firstname, surname = fio[:3]

        # Шаг 2: Обработка телефона
        phone = contact[5]
        phone_pattern = re.compile(
            r'(\+7|8)\s*\(?(\d{3})\)?[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s*\(?(доб\.?)\s*(\d+)\)?)?'
        )
        phone_match = phone_pattern.search(phone)
        if phone_match:
            formatted_phone = (
                f"+7({phone_match.group(2)}){phone_match.group(3)}-"
                f"{phone_match.group(4)}-{phone_match.group(5)}"
            )
            if phone_match.group(7):
                formatted_phone += f" доб.{phone_match.group(8)}"
            contact[5] = formatted_phone

        # Создаем обработанную запись
        processed_contact = [
            lastname, firstname, surname,
            contact[3], contact[4], contact[5], contact[6]
        ]
        processed_contacts.append(processed_contact)

    # Шаг 3: Объединение дубликатов
    unique_contacts = {}
    for contact in processed_contacts:
        key = (contact[0], contact[1])  # Фамилия и Имя как ключ
        if key not in unique_contacts:
            unique_contacts[key] = contact
        else:
            # Объединяем информацию, отдавая предпочтение непустым полям
            existing = unique_contacts[key]
            for i in range(2, 7):
                if not existing[i] and contact[i]:
                    existing[i] = contact[i]

    return list(unique_contacts.values())


# Читаем исходные данные
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Обрабатываем данные
cleaned_contacts = process_contacts(contacts_list)

# Сохраняем результат
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerows(cleaned_contacts)

print("Обработка завершена. Результат сохранен в phonebook.csv")