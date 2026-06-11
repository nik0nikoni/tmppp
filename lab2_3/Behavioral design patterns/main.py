from command import (
    Light,
    TurnOnCommand,
    TurnOffCommand,
    RemoteControl
)

from observer import (
    Course,
    Student
)

from state import (
    Order
)

from strategy import (
    PaymentContext,
    CardPayment,
    CashPayment
)


# =========================
# COMMAND
# =========================
def run_command():
    print("\n=== COMMAND ===")

    light = Light()

    on_command = TurnOnCommand(light)
    off_command = TurnOffCommand(light)

    remote = RemoteControl(on_command)
    print(remote.press_button())

    remote.command = off_command
    print(remote.press_button())


# =========================
# OBSERVER
# =========================
def run_observer():
    print("\n=== OBSERVER ===")

    course = Course()

    student1 = Student("Andrei")
    student2 = Student("Maria")

    course.subscribe(student1)
    course.subscribe(student2)

    course.notify("Новый урок доступен!")


# =========================
# STATE
# =========================
def run_state():
    print("\n=== STATE ===")

    order = Order()

    print(order.status())

    order.next()
    print(order.status())

    order.next()
    print(order.status())


# =========================
# STRATEGY
# =========================
def run_strategy():
    print("\n=== STRATEGY ===")

    context = PaymentContext(CardPayment())
    print(context.execute_payment(100))

    context.strategy = CashPayment()
    print(context.execute_payment(100))


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    run_command()
    run_observer()
    run_state()
    run_strategy()