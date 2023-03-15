from datetime import datetime, timedelta

LST = [{"name": "Jasey", "birthday": "1990-3-19"},
       {"name": "Jasey_4", "birthday": "1990-4-19"},
       {"name": "Andy", "birthday": "1990-3-18"},
       {"name": "Bill", "birthday": "1990-3-25"},
       {"name": "Brayan", "birthday": "1990-3-24"},
       {"name": "Bily", "birthday": "1990-3-23"},
       {"name": "Lisa", "birthday": "1996-2-20"},
       {"name": "Bob", "birthday": "2000-3-20"},
       {"name": "Jake", "birthday": "2000-3-16"}]

day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def get_birthdays_per_week(birthday_list: list[dict[str:str]]) -> dict:
    result_dict = {}

    today = datetime.today().date()
    next_monday = today + timedelta(days=(7 - today.weekday()))

    days_of_week = [next_monday + timedelta(days=i) for i in range(-2, 7 - 2)]

    for birthday_dict in birthday_list:

        lst_b_person = birthday_dict['birthday'].split("-")

        person_birthday = datetime(year=int(lst_b_person[0]), month=int(lst_b_person[1]), day=int(lst_b_person[2]))

        if person_birthday.month == today.month:

            birthday_in_this_year = datetime(year=today.year, month=person_birthday.month, day=person_birthday.day).date()

            if birthday_in_this_year in days_of_week:

                day_week_day = birthday_in_this_year.weekday()

                if day_week_day in (5, 6):
                    day_week_day = 0

                if result_dict.get(day_week_day):
                    result_dict[day_week_day].append(birthday_dict['name'])
                else:
                    result_dict.update({day_week_day: [birthday_dict['name']]})

    sorted_keys_list = sorted(result_dict)

    result = {}
    for k in sorted_keys_list:
        result.update({k: result_dict[k]})

    return result


if __name__ == "__main__":

    result_dict = get_birthdays_per_week(LST)
    for k, v in result_dict.items():
        print(f"{day_names[k]}: {', '.join(v)}")
