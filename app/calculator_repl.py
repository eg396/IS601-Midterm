## calculator_repl.py
## IS 601 Midterm
## Evan Garvey

from decimal import Decimal
from app.calculator import Calculator
from app.exceptions import OperationError, ValidationError
from app.history import AutoSaveObserver
from app.operations import OperationFactory
from colorama import init, Fore, Style

init(convert=True)

def calculator_repl():

    calc = None

    try:

        calc = Calculator()
        calc.add_observer(AutoSaveObserver(str(calc.config.history_file)))
        print("Calculator started. Type 'help' for commands.")

        while True:

            try:

                command = input("\nEnter command: ").lower().strip()

                if command == 'help':

                    print(Fore.CYAN + Style.BRIGHT)
                    print("\nAvailable commands:")
                    print("    add, subtract, multiply, divide, power, root,")
                    print("    modulo, int_divide, percent, abs_diff:")
                    print("      - Perform calculations.")
                    print("    history:")
                    print("      - Show history.")
                    print("    clear:")
                    print("      - Clear history.")
                    print("    undo:")
                    print("      - Undo last calculation.")
                    print("    redo:")
                    print("      - Redo last calculation.")
                    print("    save:")
                    print("      - Save history to file.")
                    print("    load:")
                    print("      - Load history from file.")
                    print("    help:")
                    print("      - Show available commands.")
                    print("    exit:")
                    print("      - Exit program.\n")
                    print(Style.RESET_ALL)
                    continue
                 
                if command == "exit":

                    try:

                        calc.save_history()
                        print("History saved to file successfully.")
                    
                    except Exception as e:

                        print(Fore.RED + Style.BRIGHT)
                        print(f"Error saving history: {e}")
                        print(Style.RESET_ALL)

                    print("Goodbye!")
                    break

                if command == "history":

                    history = calc.show_history()
                    if not history:

                        print(Fore.YELLOW + Style.BRIGHT)
                        print("History is empty.")
                        print(Style.RESET_ALL)

                    else:

                        print("\nHistory:")
                        for i, entry in enumerate(history, 1):

                            print(f"{i}. {entry}")
                                  
                    continue
                
                if command == "clear":

                    calc.clear_history()
                    print("History cleared.")
                    continue

                if command == "undo":

                    if calc.undo():

                        print("Last calculation undone.")

                    else:

                        print(Fore.YELLOW + Style.BRIGHT)
                        print("No calculations to undo.")
                        print(Style.RESET_ALL)

                    continue

                if command == "redo":

                    if calc.redo():

                        print("Last calculation redone.")

                    else:

                        print(Fore.YELLOW + Style.BRIGHT)
                        print("No calculations to redo.")
                        print(Style.RESET_ALL)

                    continue

                if command == "save":

                    try:

                        calc.save_history()
                        print("History saved to file successfully.")

                    except Exception as e:

                        print(Fore.RED + Style.BRIGHT)
                        print(f"Error saving history: {e}")
                        print(Style.RESET_ALL)

                    continue

                if command == "load":

                    try:

                        calc.load_history()
                        print("History loaded from file successfully.")

                    except Exception as e:

                        print(Fore.RED + Style.BRIGHT)
                        print(f"Error loading history: {e}")
                        print(Style.RESET_ALL)

                    continue

                if command in ['add', 'subtract', 'multiply', 'divide', 'power', 'root', 'modulo', 'int_divide', 'percent', 'abs_diff']:

                    try:

                        print("\nEnter numbers (or 'cancel' to abort):")
                        num1 = input("Number 1: ")
                        if num1.lower() == "cancel":

                            print("Calculation cancelled.")
                            continue

                        num2 = input("Number 2: ")
                        if num2.lower() == "cancel":

                            print("Calculation cancelled.")
                            continue

                        operation = OperationFactory.create(command)
                        calc.set_operation(operation)
                        result = calc.perform_operation(num1, num2)
                        if isinstance(result, Decimal):

                            result = result.normalize()

                        print(Fore.GREEN + Style.BRIGHT)
                        print(f"Result: {result}")
                        print(Style.RESET_ALL)

                    except (ValidationError, OperationError) as e:

                        print(f"Error: {e}")

                    except Exception as e:

                        print(f"Unexpected error: {e}")

                    continue

                print(Fore.YELLOW + Style.BRIGHT)
                print(f"Unknown command: {command}. type 'help' for commands.")
                print(Style.RESET_ALL)

            except KeyboardInterrupt:

                print(Fore.YELLOW + Style.BRIGHT)
                print("\nOperation cancelled: KeyboardInterrupt detected.")
                print(Style.RESET_ALL)
                continue

            except EOFError:

                print(Fore.RED + Style.BRIGHT)
                print("\nEOFError detected: terminating program...")
                print(Style.RESET_ALL)
                break

            except Exception as e:

                print(Fore.RED + Style.BRIGHT)
                print(f"Error: {e}")
                print(Style.RESET_ALL)

    except Exception as e:

        print(Fore.RED + Style.BRIGHT)
        print(f"Fatal error during initialization: {e}")
        print(Style.RESET_ALL)
        if calc is not None:

            calc._send_message(40, f"Fatal error during initialization: {e}")

        raise