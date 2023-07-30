from datetime import datetime
#creat new file named "tickets_txt"
def login():#function to get usee's username and password.
    print("Welcome to the Login Page!")
    username = input("Please enter a username: ")
    password = input("Please enter a password: ")
  
    if username == "Admin".lower() and password == "Admin123123".lower():
      return "Admin"
   #to check if the admin entered empty password, hence its a normal user
    elif password == "":
      return "User"
    else :
      None
 ##########
def get_max_ticket_info(ticket_list):
    max_ticket_number = 0
    max_priority = 0

    for ticket in ticket_list:
        ticket_id, event_id, username, date_of_event, priority = ticket
        ticket_number = int(ticket_id[4:])  # Extract the ticket number from the ticket ID
        max_ticket_number = max(max_ticket_number, ticket_number)
        max_priority = max(max_priority, int(priority))  # Convert priority to integer for comparison

    return max_ticket_number, max_priority     
##########      
def displayStatistics(ticket_list):
    max_ticket_number, max_priority = get_max_ticket_info(ticket_list)
    event_tickets_count = {}  # Dictionary to store event ID and its ticket count

    for ticket in ticket_list:
        ticket_id, event_id, username, date_of_event, priority = ticket
        if event_id not in event_tickets_count:
            event_tickets_count[event_id] = 0
        event_tickets_count[event_id] += 1

    if event_tickets_count:
        highest_ticket_count = max(event_tickets_count.values())
        event_with_highest_tickets = [event_id for event_id, count in event_tickets_count.items() if count == highest_ticket_count]

        if event_with_highest_tickets:
            print("The Event ID with the highest number of tickets:")
            print(event_with_highest_tickets[0])  # Only print the first event_id with the highest tickets
        else:
            print("No tickets found.")
    else:
        print("No tickets found.")
def futureEvents(event_date):
    # Check if the event_date is greater than or equal to today's date
    today = datetime.now().strftime("%Y%m%d")
    return event_date >= today  
########## 
def displayAllTickets(ticket_list):
    with open("tickets_txt", "r") as file:
        ticket_list = [line.strip().split(', ') for line in file if len(line.strip().split(', ')) == 5 ]
    if not ticket_list:
        print("No tickets found.")
    else:
        print("All Tickets: ")
        today = datetime.now().strftime("%Y%m%d")
        #gives today's date in the format "YYYYMMDD" for easy comparison with the ticket's date_of_event.
       # the resource of lambda function: https://sparkbyexamples.com/python/sort-using-lambda-in-python/#:~:text=A%20lambda%20function%20is%20a,to%20execute%20an%20anonymous%20function.
        # Filter and sort the tickets based on event date and event ID
        sorted_tickets = sorted(ticket_list, key=lambda x: (futureEvents(x[3]), x[3], x[1]))
 #we sort by future events first, then by event date, and finally by event ID    
        for ticket in sorted_tickets:
          ticket_id, event_id, username, date_of_event, priority = ticket
          if futureEvents(date_of_event):
            print("Ticket ID: " + ticket_id)
            print("Event ID: " + event_id)
            print("Username: " + username)
            print("Date of Event: " + date_of_event)
            print("Priority: " + priority)
            print("-" * 25) 
########## 
def changeTicketsPriority(ticket_list):
    ticket_id_to_change = input("Enter the ticket ID of the ticket you want to change priority for: ")
    new_priority = input("Enter the new priority for the changed ticket: ")
    # Find the ticket with the specified ticket ID
    found_ticket = False
    for i, ticket in enumerate(ticket_list):
        ticket_id, event_id, username, date_of_event, priority = ticket
        if ticket_id == ticket_id_to_change:
            ticket_list[i] = (ticket_id, event_id, username, date_of_event, new_priority)
            found_ticket = True
            break

    if found_ticket:
        saveTickets(ticket_list, "tickets_txt")
        print("Priority updated successfully!")
    else:
        print("Ticket not found! Please enter a valid ticket ID.")

########## 
def disableTicket(ticket_list):
    ticket_id_to_remove = input("Enter the ticket ID of the ticket you want to remove: ")

    found_ticket = False
    for ticket in ticket_list:
        if ticket[0] == ticket_id_to_remove:
            ticket_list.remove(ticket)
            found_ticket = True
            break

    if found_ticket:
        saveTickets(ticket_list, "tickets_txt")
        print("Ticket removed successfully!")
    else:
        print("Ticket not found. Please enter a valid ticket ID.")

########## 
def runEvents(ticket_list):
    today = datetime.now().strftime("%Y%m%d")

    today_events = []
    for ticket in ticket_list:
        ticket_id, event_id, username, date_of_event, priority = ticket
        if date_of_event == today:
            today_events.append(ticket)

    if not today_events:
        print("No events found for today.")
        return

    # Sort the events by priority
    today_events.sort(key=lambda x: int(x[-1]))

    print("Today's Events sorted by priority:")
    for event in today_events:
        print("Ticket ID: " + event[0] + ", Event ID: " + event[1] + ", Username: " + event[2] + ", Priority: " + event[4])
    # Remove today's events from the main ticket_list
    ticket_list = [ticket for ticket in ticket_list if ticket not in today_events]
    # Save the updated ticket_list to the text file
    saveTickets(ticket_list, "tickets_txt")
########## 
def saveTickets(ticket_list, tickets_txt):#function to save the tickets in the file
    with open(tickets_txt, 'w') as file:
        for ticket in ticket_list:
            ticket_id, event_id, username, event_datetime, priority = ticket
            formatted_event_id = "ev" + str(event_id).zfill(3)
            file.write(ticket_id + "," + formatted_event_id + "," + username + "," + event_datetime + "," + str(priority) + "\n")
########## 
def bookATicket(ticket_list):#function to book a ticket and save it on the file
    max_ticket_number, max_priority = get_max_ticket_info(ticket_list)
    username = input("Enter your username: ")
    event_id = input("Enter the ID of the event: " + "ev")
    date_of_event = input("Enter the date of the event (YYYYMMDD): ")

    priority = max_priority + 1
#https://www.w3schools.com/python/ref_string_zfill.asp
    new_ticket_id = "tick" + str(max_ticket_number + 1).zfill(3)
    ticket_list.append((new_ticket_id, event_id, username, date_of_event, priority))
    saveTickets(ticket_list, "tickets_txt")
    print("Ticket booked successfully!")

##########
# Function to display the admin menu and handle admin actions
def displayAdminMenu():
  print("This is the Admin Menu, choose what do you want to do:\nAdmin Menu: \n1. Display Statistics\n2. Book a Ticket \n3. Display all Tickets  \n4. Change Ticket’s Priority  \n5. Disable Ticket  \n6. Run Events\n7. Exit")
##########
# Function to display the user menu and handle admin actions
def displayUserMenu():
  print("This is the User Menu, choose what do you want to do:\nUser Menu:  \n1. Book a ticket\n2. Exit")
########## 
def main():
    name = input("Enter your name please: ")
    print("Welcome here,", name, "!")
    user_type = input("Enter whether you are an admin or a user: ").lower()
    # Create an empty list to hold the tickets
    ticket_list = []

    # Load tickets from the text file into the list
    with open("tickets_txt", 'r') as file:
        for line in file:
            ticket_data = line.strip().split(',')
            ticket_list.append(tuple(ticket_data))
    if user_type == "admin":
        user_role = login()
        if user_role == "Admin":
            # Display admin menu
            while True:
                displayAdminMenu()
                choice = int(input("Enter the number corresponding to the operation you want to perform (1-7): "))
                if choice == 1:
                    displayStatistics(ticket_list)
                elif choice == 2:
                    bookATicket(ticket_list)
                elif choice == 3:
                    displayAllTickets(ticket_list)
                elif choice == 4:
                    changeTicketsPriority(ticket_list)
                elif choice == 5:
                    disableTicket(ticket_list)
                elif choice == 6:
                    runEvents(ticket_list)
                elif choice == 7:
                    print("Exiting...")
                    break
                else:
                    print("Invalid input. Please try again.")
        else:
            print("Incorrect Username and/or Password. Exiting the program...")

    elif user_type == "user":
        user_role = login()
        if user_role == "User":
            displayUserMenu()
            while True:
                choice = int(input("Enter the number corresponding to the operation you want to perform (1-2): "))
                if choice == 1:
                    bookATicket(ticket_list)
                elif choice == 2:
                    print("Exiting the program...")
                    break
                else:
                    print("Invalid input. Please try again.")
        else:
            print("Incorrect Username and/or Password. Exitingthe program...")

    else:
        print("Invalid user type. Please enter 'admin' or 'user.'")

if __name__ == "__main__":
    main()
