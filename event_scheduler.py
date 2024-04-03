import re
from datetime import datetime
from operator import itemgetter


def str_to_datetime(date_str, time_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()
        return datetime.combine(date, time)
    except ValueError:
        return None


def add_event(events, title, description, date_str, time_str):
    event_date = str_to_datetime(date_str, time_str)
    if event_date is None:
        return "Invalid date or time format. Please use YYYY-MM-DD for date and HH:MM for time."

    new_event = {'title': title, 'description': description, 'date': event_date}
    events.append(new_event)
    events.sort(key=itemgetter('date'))
    return "Event added successfully."


def display_events(events):
    if not events:
        print("No events found.")
        return

    print("Title | Description | Date & Time")
    for event in events:
        print(f"{event['title']} | {event['description']} | {event['date'].strftime('%Y-%m-%d %H:%M')}")


def delete_event(events, title):
    for i, event in enumerate(events):
        if event['title'] == title:
            del events[i]
            return "Event deleted successfully."

    return "Event not found."


def search_events(events, keyword, date=None):
    results = []
    for event in events:
        if keyword.lower() in event['title'].lower() or keyword.lower() in event['description'].lower():
            results.append(event)
        if date and event['date'] == date:
            results.append(event)
    return results


def edit_event(events, title, new_title=None, new_description=None, new_date=None, new_time=None):
    for event in events:
        if event['title'] == title:
            updated_event = event.copy()
            if new_title:
                updated_event['title'] = new_title
            if new_description:
                updated_event['description'] = new_description
            if new_date and new_time:
                updated_event['date'] = str_to_datetime(new_date, new_time)

            events.remove(event)
            events.append(updated_event)
            events.sort(key=itemgetter('date'))
            return "Event updated successfully."

    return "Event not found."


if __name__ == '__main__':
    events = []
    while True:
        print("\nOptions:")
        print("1. Add event")
        print("2. List events")
        print("3. Delete event")
        print("4. Edit event")
        print("5. Search events")
        print("6. Exit")

        option = input("Enter your choice: ")

        if option == '1':
            title = input("Enter the title: ")
            description = input("Enter the description: ")
            date_str = input("Enter the date (YYYY-MM-DD): ")
            time_str = input("Enter the time (HH:MM): ")
            print(add_event(events, title, description, date_str, time_str))

        elif option == '2':
            display_events(events)

        elif option == '3':
            title = input("Enter the title of the event to delete: ")
            print(delete_event(events, title))

        elif option == '4':
            title = input("Enter the title of the event to edit: ")
            new_title = input("Enter the new title (leave blank to keep the same): ")
            new_description = input("Enter the new description (leave blank to keep the same): ")
            new_date_str = input("Enter the new date (YYYY-MM-DD, leave blank to keep the same): ")
            new_time_str = input("Enter the new time (HH:MM, leave blank to keep the same): ")

            new_date = None if new_date_str == '' else str_to_datetime(new_date_str, new_time_str)

            print(edit_event(events, title, new_title, new_description, new_date))

        elif option == '5':
            keyword = input("Enter the keyword to search: ")
            date_str = input("Enter the date to search (YYYY-MM-DD): ")
            date = datetime.strptime(date_str, '%Y-%m-%d') if date_str != '' else None
            search_results = search_events(events, keyword, date)
            print("Search Results:")
            display_events(search_results)

        elif option == '6':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")