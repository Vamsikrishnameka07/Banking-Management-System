class account:   # Class representing a bank account
    def __init__(self, accountnumber, fname, lname, password, balance):
        self.accountnumber = accountnumber
        self.fname = fname
        self.lname = lname
        self.password = password
        self.balance = balance
        self.transactions = []  # List to store transactions

class Node:     # Class representing a node in the linked list that stores accounts
    def __init__(self, account):
        self.account = account
        self.child_tree = AVLtree()      # AVL tree to store child accounts
        self.child = None       # Reference to the root of the child AVL tree
        self.next = None        # Reference to the next node in the linked list

    def add_child(self, child_node):    # Function to add a child account to the AVL tree
        self.child = self.child_tree.insert(self.child, child_node.account)


class AVLnode:  # Class representing a node in an AVL tree, which stores an account
    def __init__(self, account):
        self.account = account
        self.left = None
        self.right = None
        self.height = 1  # Height of the node for balancing

class AVLtree:# Class representing the AVL tree
    def insert(self, root, account): # Function to insert an account into the AVL tree
        if not root:
            return AVLnode(account)
        elif account.accountnumber < root.account.accountnumber:
            root.left = self.insert(root.left, account)
        else:
            root.right = self.insert(root.right, account)
        root.height = 1 + max(self.getheight(root.left), self.getheight(root.right))    # Update the height of the ancestor node

        balance = self.getbalance(root)         # Get the balance factor
       
        if balance > 1 and account.accountnumber < root.left.account.accountnumber:     # Balance the tree if needed
            return self.right_rotate(root)
        elif balance < -1 and account.accountnumber > root.right.account.accountnumber:
            return self.left_rotate(root)
        elif balance > 1 and account.accountnumber > root.left.account.accountnumber:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        elif balance < -1 and account.accountnumber < root.right.account.accountnumber:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)
        return root
    
    def left_rotate(self, x):       # Function to perform a left rotation
        y = x.right              # Set y to be the right child of x
        k = y.left              # Set k to be the left child of y (this will become the new right child of x)

        y.left = x
        x.right = k

        x.height = 1 + max(self.getheight(x.left), self.getheight(x.right))     # Update the heights of x and y
        y.height = 1 + max(self.getheight(y.left), self.getheight(y.right))

        return y
    
    def right_rotate(self, x):      # Function to perform a right rotation
        y = x.left              # Set y to be the left child of x
        k = y.right             # Set k to be the right child of y (this will become the new left child of x)


        y.right = x
        x.left = k

        x.height = 1 + max(self.getheight(x.left), self.getheight(x.right))     # Update the heights of x and y
        y.height = 1 + max(self.getheight(y.left), self.getheight(y.right))

        return y
    
    def getheight(self, x):     # Function to get the height of a node
        if not x:
            return 0
        return x.height
    
    def getbalance(self, x):    # Function to get the balance factor of a node
        if not x:
            return 0
        return self.getheight(x.left) - self.getheight(x.right)
    
    def search(self, root, accountnumber): # Function to search for an account in the AVL tree
        if not root or root.account.accountnumber == accountnumber:
            return root
        elif accountnumber < root.account.accountnumber:
            return self.search(root.left, accountnumber)
        else:
            return self.search(root.right, accountnumber)

    def traversal(self, root):      # Function to traverse the AVL tree and print account details
        if root:
            print("\nAccount Number: ", root.account.accountnumber)
            print("\nFirst Name: ", root.account.fname)
            print("\nLast Name: ", root.account.lname)
            print("\nBalance: ", root.account.balance)
            print("\n___")
            self.traversal(root.left)
            self.traversal(root.right)


class BankingMangementSystem:       # Class representing the banking management system
    def __init__(self):
        self.head = None  # Reference to the head of the linked list of accounts

    def Addaccount(self):
        age_str = input("Are you more than 18 years old? (y/n): ").lower()
        if age_str == "y":      # For users above 18, create a parent account
            accountnumber = input("Enter Account Number: ")
            if self.isUnique(accountnumber):
                account_details = self.get_account_details(accountnumber)
                parentnode = Node(account(**account_details))      #Node is created 
                if self.head is None:                   #Parent Node is linked to end of linked list
                    self.head = parentnode
                else:
                    curr = self.head
                    while curr.next:
                        curr = curr.next
                    curr.next = parentnode
                print("Account added Successfully.")
            else:
                print("Account already exists.")
        else:       # For users below 18, create a child account
            parent_account_number = input("Enter Parent Account Number: ")
            parent_node = self.findaccount1(parent_account_number)
            if parent_node:
                accountnumber = input("Enter Account Number: ")
                if self.isUnique(accountnumber):
                    account_details = self.get_account_details(accountnumber)
                    child_node = Node(account(**account_details))          #Node is created 
                    parent_node.add_child(child_node)                   #Function call of add_child
                    print("Minor Account created and linked to parent account.")
                else:
                    print("Account already exists")
            else:
                print("Parent account not found.")

    def get_account_details(self,accountnumber):          #Enter details of New Account
        account_details = {
            'accountnumber': accountnumber,
            'fname': input("Enter First Name: "),
            'lname': input("Enter Last Name: "),
            'password': input("Enter Password: "),
            'balance': float(input("Enter First Deposit: "))
        }
        return account_details

    def isUnique(self, accno):      # Function to check if an account number is unique
        curr = self.head
        while curr:
            if curr.account.accountnumber == accno:
                return False
            curr = curr.next
        return True

    def findaccount(self, accno, passwd):       # Function to find an account with account number and password
        curr = self.head
        while curr:
            if curr.account.accountnumber == accno and curr.account.password == passwd:
                return curr
            curr = curr.next
        return None
    
    def findaccount1(self, accno):      # Function to find an account with account number
        curr = self.head
        while curr:
            if curr.account.accountnumber == accno:
                return curr
            curr = curr.next
        return None

    def findchildaccount1(self, child_accno):       # Function to find a child account with account number
        curr = self.head
        while curr:
            child_node = curr.child_tree.search(curr.child, child_accno)
            if child_node:
                return child_node
            curr = curr.next
        return None

    def findchildaccount(self, child_accno, passwd):        # Function to find a child account with account number and password
        curr = self.head
        while curr:
            child_node = curr.child_tree.search(curr.child, child_accno)
            if child_node and child_node.account.password == passwd:
                return child_node
            curr = curr.next
        return None

    def searchaccount(self):       # Function to search for an account
        accno, passwd = input("Enter Account number: "), input("Enter Password: ")
        account = self.findaccount(accno, passwd)  # Search for the main account
        if account:
            self.print_account_details(account)  # Print account details if found
        else:
            childaccount = self.findchildaccount(accno, passwd)  # Search for the child account
            if childaccount:
                self.print_account_details(childaccount)  # Print account details if found
            else:
                print("\nAccount Not Found or Password Incorrect")

    def depositmoney(self):      # Function to deposit money into an account
        accno = input("Enter Account number: ")
        account = self.findaccount1(accno)
        if not account:
            account = self.findchildaccount1(accno)  # Check if the account is a minor account
        if account:
            deposit = float(input("Enter the amount to be Deposited: "))
            account.account.balance += deposit  # Add the deposit amount to the balance
            account.account.transactions.append(f"Deposit: +{deposit}")  # Record the transaction
            print("\nMoney successfully deposited")
        else:
            print("\nAccount Not Found")

    def withdrawMoney(self):        # Function to withdraw money from an account
        accno, passwd = input("Enter Account number: "), input("Enter Password: ")
        account = self.findaccount(accno, passwd) or self.findchildaccount(accno, passwd)  # Search for the account
        if account:
            withdraw = float(input("Enter the amount to be Withdrawn: "))
            if withdraw <= account.account.balance:
                account.account.balance -= withdraw  # Subtract the withdrawal amount from the balance
                account.account.transactions.append(f"Withdraw: -{withdraw}")  # Record the transaction
                print("\nMoney successfully withdrawn")
            else:
                print("\nInsufficient Balance")
        else:
            print("\nAccount Not Found or Password Incorrect")

    def print_account_details(self,account):# Function to print account details
        print("\nAccount Number: ", account.account.accountnumber)
        print("\nFirst Name: ", account.account.fname)
        print("\nLast Name: ", account.account.lname)
        print("\nBalance: ", account.account.balance)

    def displayallMajoraccounts(self):      # Function to display all major accounts
        print("\n ___ALL ACCOUNTS___")
        curr = self.head
        while curr is not None:
            print("\nAccount Number: ", curr.account.accountnumber)
            print("\nFirst Name: ", curr.account.fname)
            print("\nLast Name: ", curr.account.lname)
            print("\nBalance: ", curr.account.balance)
            print("\n---")
            curr = curr.next

    def displayallMinoraccounts(self):      # Function to display all minor accounts
        curr = self.head
        while curr:
            child_node = curr.child
            print("\n___Minor Accounts Linked to Major Account: ", curr.account.accountnumber, "___")
            curr.child_tree.traversal(child_node)
            curr = curr.next
        return None

    def transfer_funds(self,sender, receiver, sender_accno, receiver_accno):        #Function to transfer funds between given accounts
        transfer_amount = float(input("Enter the amount to transfer: "))
        if transfer_amount <= sender.account.balance:
            sender.account.balance -= transfer_amount
            receiver.account.balance += transfer_amount
            sender.account.transactions.append(f"Transfer: -{transfer_amount} To accno:{receiver_accno}")
            receiver.account.transactions.append(f"Transfer: +{transfer_amount} From accno:{sender_accno}")
            print("Money transferred successfully.")
        else:
            print("Insufficient balance in sender's account.")

    def transferMoney(self):            # Function to transfer money between accounts
        sender_accno = input("Enter sender's Account number: ")
        sender_passwd = input("Enter sender's Password: ")
        receiver_accno = input("Enter receiver's Account number: ")

        sender_account = self.findaccount(sender_accno, sender_passwd)
        receiver_account = self.findaccount1(receiver_accno)
        c_sender_account = self.findchildaccount(sender_accno, sender_passwd)
        c_receiver_account = self.findchildaccount1(receiver_accno)

        if sender_account and receiver_account:
            self.transfer_funds(sender_account, receiver_account, sender_accno, receiver_accno)
        elif c_sender_account and c_receiver_account:
            self.transfer_funds(c_sender_account, c_receiver_account, sender_accno, receiver_accno)
        elif c_sender_account and receiver_account:
            self.transfer_funds(c_sender_account, receiver_account, sender_accno, receiver_accno)
        elif sender_account and c_receiver_account:
            self.transfer_funds(sender_account, c_receiver_account, sender_accno, receiver_accno)
        else:
            print("Sender's or Receiver's account not found or incorrect password.")

    def last10Transactions(self, account):      # Function to retrieve money transfers between accounts
        if len(account.account.transactions) <= 10:
            return account.account.transactions
        else:
            return account.account.transactions[-10:]

    def displayTransactions(self):      # Function to display the last 10 transactions of an account
        accno = input("Enter Account Number: ")
        passwd = input("Enter password: ")
        account = self.findaccount(accno, passwd)
        c_account = self.findchildaccount(accno, passwd)
        if account:
            L_10_Transactions = self.last10Transactions(account)        #store last 10 transactions that are returned
            print("\nLast 10 Transactions")
            for transaction in L_10_Transactions:           #print the transactions
                print(transaction)
        elif c_account:
            L_10_Transactions = self.last10Transactions(c_account)      #store last 10 transactions that are returned
            print("\nLast 10 Transactions")
            for transaction in L_10_Transactions:           #print the  transactions
                print(transaction)
        else:
            print("\nAccount Not Found or Password Incorrect")

class ATMGraph:
    def __init__(self):
        self.vertices = {}  # Initialize the vertices dictionary to store vertices and their edges

    def add_vertex(self, name, location):
        if name not in self.vertices:  # Check if the vertex already exists
            self.vertices[name] = {'location': location, 'edges': {}}  # Add the vertex with its location and an empty edge dictionary

    def add_edge(self, source, destination, distance):
        if source in self.vertices and destination in self.vertices:  # Check if both source and destination vertices exist
            self.vertices[source]['edges'][destination] = distance  # Add the edge from source to destination with distance
            self.vertices[destination]['edges'][source] = distance  # Add the edge from destination to source with distance

    def get_distance(self, source, destination):
        if source in self.vertices and destination in self.vertices[source]['edges']:  # Check if both source and destination vertices exist, and if there is an edge between them
            return self.vertices[source]['edges'][destination]  # Return the distance between the source and destination vertices
        return None  # Return None if there is no edge between the vertices or if one of the vertices doesn't exist

    def display(self):
        for vertex in self.vertices:
            print(vertex, ":", self.vertices[vertex])  # Display the vertices and their edges
  
class ATM:
    def __init__(self):
        self.atm_graph = ATMGraph()

    def nearestAtm(self):
        default_atms = {            # Add default ATM locations in each city
        
            'Hyderabad': {
                'ATM 1': (17.4, 78.5),'ATM 2': (17.4, 78.3),'ATM 3': (17.4, 78.4),'ATM 4': (17.4, 78.5),'ATM 5': (17.4, 78.4)
            },
            'Bangalore': {
                'ATM 6': (12.9, 77.2),'ATM 7': (12.9, 77.3),'ATM 8': (12.9, 77.1),'ATM 9': (12.9, 77.4),'ATM 10': (12.9, 77.5)
            },
            'Chennai': {
                'ATM 11': (13.1, 80.4),'ATM 12': (13.1, 80.5),'ATM 13': (13.1, 80.2),'ATM 14': (13.1, 80.1),'ATM 15': (13.1, 80.6)
            }
        }

        for city, atms in default_atms.items():          # Iterate over each city and its ATMs in the DEFAULT_ATMS dictionary
            for atm, location in atms.items():          # Iterate over each ATM and its location in the city's ATM dictionary
                self.atm_graph.add_vertex(atm, location)         # Add each ATM as a vertex to the graph with its location

        default_places = {          # Add default places in each city
            'Hyderabad': {
                'Panjagutta': (17.4, 78.1),'Jubilee Hills': (17.4, 78.2),'Ameerpet': (17.4, 78.2),'Hitech City': (17.4, 78.6)
            },
            'Bangalore': {
                'Koramangala': (12.9, 77.6),'Indiranagar': (12.9, 77.7),'MG Road': (12.9, 77.8),'Whitefield': (12.9, 77.7)
            },
            'Chennai': {
                'T Nagar': (13.1, 80.3),'Anna Nagar': (13.1, 80.4),'Adyar': (13.1, 80.0),'Nungambakkam': (13.1, 80.7)
            }
        }
        for city, places in default_places.items():        # Iterate over each city and its places in the DEFAULT_ATMS dictionary
            for place, location in places.items():          # Iterate over each place and its location in the city's ATM dictionary
                self.atm_graph.add_vertex(place, location)          # Add each ATM as a vertex to the graph with its location

        for city in default_atms.keys():        # Add distances between default places and ATMs
            for atm in default_atms[city]:
                for place in default_places[city]:
                    distance = ((default_atms[city][atm][0] - default_places[city][place][0]) ** 2 +                #distance calulated between 2 points is [(x1 - x2)^2 + (y1 - y2)^2]^0.5
                                (default_atms[city][atm][1] - default_places[city][place][1]) ** 2) ** 0.5
                    self.atm_graph.add_edge(atm, place, distance)

        city = input("Enter city (Hyderabad, Bangalore, Chennai): ")
        if city in default_places:
            place = input(f"Enter a place in {city}: ")
            if place in default_places[city]:
                nearest_atm = None          # Find the nearest ATM by minimum distance
                min_distance = float('inf')
                for atm in default_atms[city]:
                    distance = self.atm_graph.get_distance(place, atm)
                    if distance is not None and distance < min_distance:
                        nearest_atm = atm
                        min_distance = distance
                if nearest_atm:
                    print(f"Nearest ATM to {place} is {nearest_atm} with a distance of {min_distance:.2f} Km.")
                else:
                    print("No ATMs found.")
            else:
                print("Invalid place.")
        else:
            print("Invalid city.")

def menu():         # Function to display the main menu and handle user choice
    bank = BankingMangementSystem()
    atm = ATM()
    while True:
        print("\n___BANKING MANAGEMENT SYSTEM___")
        print("\n1. Add Account")
        print("\n2. Search Account")
        print("\n3. Deposit Funds")
        print("\n4. Withdraw Funds")
        print("\n5. Display All Major Accounts")
        print("\n6. Display All Minor Accounts")
        print("\n7. Transfer money")
        print("\n8. Display Last 10 Transactions")
        print("\n9. Display Nearest ATM")
        print("\n10. Exit")
        choice = int(input())

        if choice == 1:
            bank.Addaccount()
        elif choice == 2:
            bank.searchaccount()
        elif choice == 3:
            bank.depositmoney()
        elif choice == 4:
            bank.withdrawMoney()
        elif choice == 5:
            bank.displayallMajoraccounts()
        elif choice == 6:
            bank.displayallMinoraccounts()
        elif choice == 7:
            bank.transferMoney()
        elif choice == 8:
            bank.displayTransactions()
        elif choice == 9:
            atm.nearestAtm()
        elif choice == 10:
            return
        else:
            print("\nInvalid choice")

def main():         # Main function to start the program
    menu()

if __name__ == "__main__":
    main()




