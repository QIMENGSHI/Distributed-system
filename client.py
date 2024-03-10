import xmlrpc.client
from datetime import datetime

def print_menu():
    print("\nMenu:")
    print("1. Add a note")
    print("2. Get notes by topic")
    print("3. Delete a text entry from a topic")
    print("4. Delete a topic")
    print("5. Search Wikipedia and add result to a topic")
    print("6. Exit")

def main():
    server_address = 'http://localhost:8000'
    with xmlrpc.client.ServerProxy(server_address) as proxy:
        while True:
            print_menu()
            choice = input("Choose an option: ")

            if choice == '1':
                topic = input("Enter topic: ")
                text = input("Enter text: ")
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                proxy.add_note(topic, text, timestamp)
                print("Note added.")

            elif choice == '2':
                topic = input("Enter topic to retrieve: ")
                print("Notes for topic:", proxy.get_notes(topic))

            elif choice == '3':
                topic = input("Enter topic: ")
                timestamp = input("Enter timestamp of the entry to delete: ")
                if proxy.delete_entry(topic, timestamp):
                    print("Entry deleted.")
                else:
                    print("Entry not found or could not be deleted.")

            elif choice == '4':
                topic = input("Enter topic to delete: ")
                if proxy.delete_topic(topic):
                    print("Topic deleted.")
                else:
                    print("Topic not found or could not be deleted.")

            elif choice == '5':
                search_term = input("Enter search term for Wikipedia: ")
                wiki_url = proxy.query_wikipedia(search_term)
                print("Wikipedia URL:", wiki_url)
                if wiki_url.startswith("http"):
                    topic = input("Enter topic to append Wikipedia URL to: ")
                    text = f"Wikipedia link: {wiki_url}"
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    proxy.add_note(topic, text, timestamp)
                    print("Wikipedia link added to topic.")
                else:
                    print("No Wikipedia article found.")

            elif choice == '6':
                print("Exiting.")
                break

            else:
                print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
