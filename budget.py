class Category:
    
    def __init__(self, name):
        self.name = name.lower()
        self.ledger = []

    def deposit(self, amnt, dscrpt=""):
        self.form = {"amount": amnt,"description": dscrpt}  
        self.ledger.append(self.form)

    def get_balance(self):
        blnc = 0
        for ledger in self.ledger:
            blnc += ledger["amount"]
        return blnc

    def check_funds(self, amnt):
        if amnt <= self.get_balance():
            return True
        else:
            return False

    def withdraw(self, amnt, dscrpt=""):
        self.form = {"amount": -amnt,"description": dscrpt} 
        if self.check_funds(amnt) == True:
            self.ledger.append(self.form)
            return True
        else:
            print("Not enough funds for withdrawl.")
            return False

    def transfer(self, amnt, dstnt):
        if self.check_funds(amnt) == True:
            self.withdraw(amnt, f"Transfer to {dstnt.name.capitalize()}")
            dstnt.deposit(amnt, f"Transfer from {self.name.capitalize()}")
            return True
        else:
            print("Not enough funds for transfer.")
            return False

    def __str__(self):
        num_stars = int((30 - len(str(self.name))) / 2)
        display_title = "*" * num_stars + self.name.capitalize() + "*" * num_stars
        budget_display = display_title + "\n"
        display_total = f"Total: {self.get_balance()}"

        for ledger in self.ledger:
            dscrpt_len = len(ledger["description"])
            if dscrpt_len < 24:
                ledger["description"] = ledger["description"] + " " * (23 - dscrpt_len)
            else:
                ledger["description"] = ledger["description"][:23]

            amnt_len = len(str('%.2f' % ledger["amount"]))
            if amnt_len < 8:
                ledger["amount"] = " " * (7 - amnt_len) + '%.2f' % ledger["amount"]
            else:
                ledger["amount"] = ledger["amount"][:7]
      
            budget_display += ledger["description"] + ledger["amount"] + "\n"

        budget_display += display_total
        return budget_display


def create_spend_chart(categories):  
    title_line = "Percentage spent by category\n"
    bar_labels = []
    for i in range(100, -10, -10):
        bar_labels.append(f"{i}|")
    bottom_line = " " * 4 + "-" * (len(categories) * 3 + 1)

    spent_dict = {}  
    total_spent = 0  
    percentage_dict = {}  
    for ctgr in categories:  
        spent = 0  
        for ledger in ctgr.ledger:  
            if float(ledger["amount"]) < 0:
                spent -= float(ledger["amount"])
        spent = round(spent, 2)
        spent_dict[ctgr.name] = spent
        total_spent += spent_dict[ctgr.name]

    for ctgr in categories:
        percentage_dict[ctgr.name] = spent_dict.get(ctgr.name) / total_spent
        percentage_dict[ctgr.name] = int(str(percentage_dict.get(ctgr.name))[2])

        j = 10
        for i in range(len(bar_labels)): 
            if percentage_dict.get(ctgr.name) >= j: bar_labels[i] += " o "
            else: bar_labels[i] += " "*3
            j -= 1
  
    vert_name = "\n"

    max_len = []
    for ctgr in categories :
        max_len.append(len(ctgr.name))
    max_len = max(max_len)
  
    frmt_name = []
    for ctgr in categories :
        Name = ctgr.name.capitalize()
        Name += " "*(max_len-len(Name))
        frmt_name.append(Name)
        
    for i in range(max_len) :
        vert_name += " "*4
        for j in range(len(categories)) : vert_name += f" {frmt_name[j][i]} "
        if i < (max_len-1): vert_name += " \n"
        else: vert_name += " "
    
    bar_lines = ""
    for bar in bar_labels:
        if bar[:4] == "100|": bar_lines += f"{bar} \n"
        elif bar[:3] == "0| ": bar_lines += f"  {bar} \n"
        else: bar_lines += f" {bar} \n"
    spend_chart = title_line + bar_lines + bottom_line + vert_name
    
    return spend_chart
