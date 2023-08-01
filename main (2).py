from datetime import datetime
#function to get usee's username and password.
#O(1)the loop runs for a constant number of iterations(5)
def login():
    print("Welcome to the Login Page!")
  
    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        username = input("Please enter a username: ").lower()
        password = input("Please enter a password: ")

        if username == "admin" and password.lower() == "admin123123":
            return "Admin"
        elif password == "":
            return "User"
        else:
            attempts += 1
            print("Incorrect Username and/or Password. Remaining attempts:", max_attempts - attempts)

    print("Maximum login attempts reached. Exiting the program.")
    return None
   #to check if the admin entered empty password, hence its a normal user

 ##########
#func to find the maximum ticket number and the highest priority among the tickets in the provided ticket_list and called In the displayStatistics().
#O(n),n being the number of tickets in the ticket_list.
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
  # function responsible for displaying statistical information about the tickets stored in the ticket_list.
#O(n), n being the len of the lis
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
#######
#O(1),constant time
# Check if the event_date is greater than or equal to today's date
def futureEvents(event_date):
    today = datetime.now().strftime("%Y%m%d")
    return event_date >= today  
#########################
def selection_sort(tickets):
    n = len(tickets)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if tickets[j][3] < tickets[min_idx][3]:
                min_idx = j
            elif tickets[j][3] == tickets[min_idx][3] and tickets[j][1] < tickets[min_idx][1]:
                min_idx = j
        tickets[i], tickets[min_idx] = tickets[min_idx], tickets[i]
###############################3
def displayAllTickets(ticket_list):
    if not ticket_list:
        print("No tickets found.")
    else:
        print("All Tickets: ")
        today = datetime.now().strftime("%Y%m%d")#gives today's date in the format "YYYYMMDD" for easy comparison with the ticket's date_of_event.
        today_tickets = [ticket for ticket in ticket_list if ticket[3] >= today]
        selection_sort(today_tickets)

        for ticket in today_tickets:
            ticket_id, event_id, username, date_of_event, priority = ticket
            print("Ticket ID: " + str(ticket_id))
            print("Event ID: " + str(event_id))
            print("Username: " + username)
            print("Date of Event: " + date_of_event)
            print("Priority: " + str(priority))  # Convert priority to a string
            print("-" * 25)
########## 
#allows the admin to change the priority of a ticket in the ticket_list
def changeTicketsPriority(ticket_list):#O(n), n being the number of tickets in the ticket_list
    ticket_id_to_change = input("Enter the ticket ID of the ticket you want to change priority for: ")
    new_priority = input("Enter the new priority for the changed ticket: ")

    # Find the ticket with the specified ticket ID
    found_ticket = False
    for i, ticket in enumerate(ticket_list):#https://www.w3schools.com/python/ref_func_enumerate.asp
        ticket_id, event_id, username, date_of_event, priority = ticket
        if ticket_id == ticket_id_to_change:
            ticket_list[i] = (ticket_id, event_id, username, date_of_event, new_priority)
            found_ticket = True
            break

    if found_ticket:
        # Save the changes to the file after updating the ticket_list
        saveTickets(ticket_list, "tickets_txt")
        print("Priority updated successfully!")
    else:
        print("Ticket not found! Please enter a valid ticket ID.")
########## 
#allows the admin to remove a ticket from the ticket_list
def disableTicket(ticket_list):#O(n), n being the len of he list
    ticket_id_to_remove = input("Enter the ticket ID of the ticket you want to remove: ")

    found_ticket = False
    for ticket in ticket_list:
        if ticket[0] == ticket_id_to_remove:
            ticket_list.remove(ticket)
            found_ticket = True
            break

    if found_ticket:
        # Save the changes to the file after removing the ticket from the ticket_list
        saveTickets(ticket_list, "tickets_txt")
        print("Ticket removed successfully!")
    else:
        print("Ticket not found. Please enter a valid ticket ID.")
########## 
  #to display and process events that are scheduled for the current day
def runEvents(ticket_list):#O(nlog n)n being the number of events for today
    today = datetime.now().strftime("%Y%m%d")
    today_events = [ticket for ticket in ticket_list if ticket[3] == today]

    if not today_events:
        print("No events found for today.")
        return

    # Sort the events by priority
    today_events.sort(key=lambda x: int(x[-1]))

    print("Today's Events sorted by priority:")
    for event in today_events:
        ticket_id, event_id, username, date_of_event, priority = event
        print("Ticket ID: " + ticket_id + ", Event ID: " + event_id + ", Username: " + username + ", Priority: " + priority)

    # Update the ticket_list to remove today's events
    ticket_list = [ticket for ticket in ticket_list if ticket not in today_events]

    # Save the updated ticket_list to the text file
    saveTickets(ticket_list, "tickets_txt")


########## 
#function to save the tickets in the txt file
def saveTickets(ticket_list, tickets_txt):#O(n),n being the number of tickets in the ticket_list.
    with open(tickets_txt, 'w') as file:
        for ticket in ticket_list:
            ticket_id, event_id, username, event_datetime, priority = ticket
            formatted_event_id = "ev" + str(event_id).zfill(3)
            file.write(ticket_id + "," + formatted_event_id + "," + username + "," + event_datetime + "," + str(priority) + "\n")
########## 
 #allow a user (admin or regular user) to book a new ticket for an event
def bookATicket(ticket_list):#O(1),constant time
    max_ticket_number, max_priority = get_max_ticket_info(ticket_list)
    username = input("Enter your username: ")
    event_id = input("Enter the ID of the event: ")
    date_of_event = input("Enter the date of the event (YYYYMMDD): ")

    priority = max_priority + 1
    new_ticket_id = "tick" + str(max_ticket_number + 1).zfill(3)#3 digit number
    formatted_event_id = "ev" + event_id

    # Add the formatted event ID when appending the ticket
    ticket_list.append((new_ticket_id, formatted_event_id, username, date_of_event, priority))
    # Save the changes to the file after adding the new ticket to the ticket_list
    saveTickets(ticket_list, "tickets_txt")
    print("Ticket booked successfully!")
##########
# Function to display the admin menu and handle admin actions
def displayAdminMenu():#O(1),constant time
    print("This is the Admin Menu, choose what do you want to do:")
    print("Admin Menu: ")
    print("1. Display Statistics")
    print("2. Book a Ticket")
    print("3. Display all Tickets")
    print("4. Change Ticket’s Priority")
    print("5. Disable Ticket")
    print("6. Run Events")
    print("7. Exit")
##########
# Function to display the user menu and handle admin actions
def displayUserMenu():#O(1),constant time
    print("This is the User Menu, choose what do you want to do:")
    print("User Menu:")
    print("1. Book a ticket")
    print("2. Exit")
########## 
def main():#O(n log n), n being the lenght conten of the list
    name = input("Enter your name, please: ")
    print("Welcome here, " + name + "!")
    
    # Create an empty list to hold the tickets
    ticket_list = []

    # Load tickets from the text file into the list
    with open("tickets_txt", 'r') as file:
        for line in file:
            ticket_data = line.strip().split(',')
            ticket_list.append(tuple(ticket_data))

    user_type = input("Enter whether you are an admin or a user: ").lower()
    user_role = login()

    if user_role == "Admin" and user_type == "admin":
        # Admin menu loop
        while True:
            displayAdminMenu()
            choice = input("Enter the number corresponding to the operation you want to perform (1-7): ")
            if choice == "1":
                displayStatistics(ticket_list)
            elif choice == "2":
                bookATicket(ticket_list)
            elif choice == "3":
                displayAllTickets(ticket_list)
            elif choice == "4":
                changeTicketsPriority(ticket_list)
            elif choice == "5":
                disableTicket(ticket_list)
            elif choice == "6":
                runEvents(ticket_list)
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid input. Please try again.")
    elif user_role == "User" and user_type == "user":
        # User menu loop
        while True:
            displayUserMenu()
            choice = input("Enter the number corresponding to the operation you want to perform (1-2): ")
            if choice == "1":
                bookATicket(ticket_list)
            elif choice == "2":
                print("Exiting the program...")
                break
            else:
                print("Invalid input. Please try again.")
    else:
        print("Incorrect Username and/or Password or invalid user type. Exiting the program...")
main()

