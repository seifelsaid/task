grammar = {}

def is_simple_grammar(grammar):
    for non_terminal, rules in grammar.items():
        first_letters = set()
        for rule in rules:
            if "ε" in rule:
                return False
            if rule[0] in first_letters:
                return False
            first_letters.add(rule[0])
    return True

def input_grammar():
    print("Enter your grammar (type 'done' when finished):")
    global grammar
    grammar = {}
    while True:
        non_terminal = input("Non-Terminal (e.g., S): ").strip().upper()
        if non_terminal.lower() == 'done':
            break
            
        rules = input(f"Rules for {non_terminal} (separated by '|'): ").strip().split('|')
        for rule in rules:
            rule = rule.strip()
            if non_terminal in grammar:
                grammar[non_terminal].append(rule)
            else:
                grammar[non_terminal] = [rule]
    if is_simple_grammar(grammar):
        print("******************************************************************")
        print("The grammar is simple.")
    else:
        print("******************************************************************")
        print("The grammar is NOT simple. Printing and deleting the grammar:")
        print("Grammar to be deleted:")
        for non_terminal, rules in grammar.items():
            for rule in rules:
                print(f"{non_terminal} → {rule}")
        grammar.clear()
        print("Grammar has been deleted.")

def print_grammar():
    print("\nGrammar:")
    for non_terminal, rules in grammar.items():
        for rule in rules:
            print(f"{non_terminal} → {rule}")

def draw_tree(sequence, stack_trace, parse_tree):
    def display_tree(node, indent="", is_last=True):
       
        prefix = "|____" if indent else ""  
        print(indent + prefix + node["symbol"])
        indent += "      " if is_last else "|      "  
        for i, child in enumerate(node["children"]):
            display_tree(child, indent, is_last=(i == len(node["children"]) - 1))

    print("\nStack trace for each input:")
    print(f"\n\nthe input is : [ {', '.join([repr(c) for c in sequence])} ]")

    print("\nStack for each input ):")
    for input_seq, stack in stack_trace:
        print(f" Current Stack: {stack}")
    print(" Current Stack: [ ]") 

    print("\nParse Tree:")
    display_tree(parse_tree)

    

def parse_string(sequence, start_symbol):
    stack = [start_symbol]
    index = 0
    stack_trace = []
    parse_tree = {"symbol": start_symbol, "children": []}
    node_stack = [parse_tree]

    while stack:
        current = stack.pop()
        current_node = node_stack.pop()
        stack_trace.append((sequence[:index], stack + [current]))

        if index < len(sequence) and current == sequence[index]:
            index += 1
        elif current in grammar:
            matched = False
            for rule in grammar[current]:
                if index < len(sequence) and rule[0] == sequence[index]:
                    stack.extend(rule[::-1])
                    matched = True
                    for symbol in rule[::-1]:
                        child_node = {"symbol": symbol, "children": []}
                        current_node["children"].append(child_node)
                        node_stack.append(child_node)
                    break
            if not matched:
                print("Sequence is Rejected.")
                return
        else:
            print("Sequence is Rejected.")
            return

    if index == len(sequence):
        print("Sequence is Accepted.")
        draw_tree(sequence, stack_trace, parse_tree)
    else:
        print("Sequence is Rejected.")


def main_menu():
    while True:
        print("\nMenu:")
        print("1. Input Grammar")
        print("2. Display Grammar")
        print("3. Parse a Sequence")
        print("4. Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            input_grammar()
        elif choice == '2':
            if not grammar:
                print("Grammar is empty. Please input a grammar first.")
            else:
                print_grammar()
        elif choice == '3':
            if not grammar:
                print("Grammar is empty. Please input a grammar first.")
                continue
            sequence = input("Enter the sequence to parse: ").strip()
            start_symbol = list(grammar.keys())[0]
            parse_string(sequence, start_symbol)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
