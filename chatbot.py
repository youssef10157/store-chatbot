import sys
from datetime import datetime


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")


PRODUCTS = {
    "\u0642\u0645\u064a\u0635 \u0642\u0637\u0646": {"price": 350, "stock": 12},
    "\u0628\u0646\u0637\u0644\u0648\u0646 \u062c\u064a\u0646\u0632": {"price": 600, "stock": 7},
    "\u062d\u0630\u0627\u0621 \u0631\u064a\u0627\u0636\u064a": {"price": 900, "stock": 5},
    "\u062d\u0642\u064a\u0628\u0629 \u064a\u0648\u0645\u064a\u0629": {"price": 450, "stock": 9},
}

cart = {}


def money(value: int) -> str:
    return f"{value} \u062c\u0646\u064a\u0647"


def product_list() -> str:
    lines = ["\u0627\u0644\u0645\u0646\u062a\u062c\u0627\u062a \u0627\u0644\u0645\u062a\u0627\u062d\u0629:"]
    for name, details in PRODUCTS.items():
        lines.append(
            f"- {name}: {money(details['price'])} (\u0627\u0644\u0645\u062a\u0627\u062d {details['stock']})"
        )
    return "\n".join(lines)


def find_product(text: str) -> str | None:
    return next((name for name in PRODUCTS if name in text), None)


def cart_summary() -> str:
    if not cart:
        return "\u0627\u0644\u0633\u0644\u0629 \u0641\u0627\u0631\u063a\u0629."

    total = 0
    lines = ["\u0645\u062d\u062a\u0648\u064a\u0627\u062a \u0627\u0644\u0633\u0644\u0629:"]
    for name, quantity in cart.items():
        line_total = PRODUCTS[name]["price"] * quantity
        total += line_total
        lines.append(f"- {name} \u00d7 {quantity} = {money(line_total)}")
    lines.append(f"\u0627\u0644\u0625\u062c\u0645\u0627\u0644\u064a: {money(total)}")
    return "\n".join(lines)


def add_to_cart(product: str, quantity: int = 1) -> str:
    available = PRODUCTS[product]["stock"] - cart.get(product, 0)
    if quantity > available:
        return f"\u0627\u0644\u0645\u062a\u0627\u062d \u0645\u0646 {product}: {available} \u0641\u0642\u0637."
    cart[product] = cart.get(product, 0) + quantity
    return f"\u062a\u0645\u062a \u0625\u0636\u0627\u0641\u0629 {quantity} \u0645\u0646 {product} \u0644\u0644\u0633\u0644\u0629.\n{cart_summary()}"


def reply(message: str) -> str:
    text = message.strip().lower()

    if not text:
        return "\u0627\u0643\u062a\u0628 \u0633\u0624\u0627\u0644\u0643 \u0623\u0648 \u0627\u0643\u062a\u0628 \u00ab\u0645\u0633\u0627\u0639\u062f\u0629\u00bb."

    if text in {"\u062e\u0631\u0648\u062c", "exit", "quit"}:
        return "\u0645\u0639 \u0627\u0644\u0633\u0644\u0627\u0645\u0629!"

    if "\u0645\u0633\u0627\u0639\u062f\u0629" in text or "\u0623\u0648\u0627\u0645\u0631" in text:
        return (
            "\u0623\u0642\u062f\u0631 \u0623\u0633\u0627\u0639\u062f\u0643 \u0641\u064a:\n"
            "- \u0627\u0643\u062a\u0628 \u00ab\u0627\u0644\u0645\u0646\u062a\u062c\u0627\u062a\u00bb \u0644\u0639\u0631\u0636 \u0627\u0644\u0643\u062a\u0627\u0644\u0648\u062c.\n"
            "- \u0627\u0643\u062a\u0628 \u00ab\u0633\u0639\u0631 \u062d\u0630\u0627\u0621 \u0631\u064a\u0627\u0636\u064a\u00bb \u0644\u0644\u0628\u062d\u062b.\n"
            "- \u0627\u0643\u062a\u0628 \u00ab\u0627\u0636\u0641 \u062d\u0630\u0627\u0621 \u0631\u064a\u0627\u0636\u064a\u00bb \u0644\u0644\u0633\u0644\u0629.\n"
            "- \u0627\u0643\u062a\u0628 \u00ab\u0627\u0644\u0633\u0644\u0629\u00bb \u0644\u0645\u0631\u0627\u062c\u0639\u0629 \u0637\u0644\u0628\u0643."
        )

    if "\u0627\u0644\u0645\u0646\u062a\u062c\u0627\u062a" in text or "\u0627\u0644\u0643\u062a\u0627\u0644\u0648\u062c" in text:
        return product_list()

    if "\u0627\u0644\u0633\u0644\u0629" in text:
        return cart_summary()

    if "\u0641\u0631\u063a \u0627\u0644\u0633\u0644\u0629" in text or "\u0645\u0633\u062d \u0627\u0644\u0633\u0644\u0629" in text:
        cart.clear()
        return "\u062a\u0645 \u062a\u0641\u0631\u064a\u063a \u0627\u0644\u0633\u0644\u0629."

    if "\u0645\u0648\u0627\u0639\u064a\u062f" in text or "\u0645\u0641\u062a\u0648\u062d" in text:
        return "\u0645\u0648\u0627\u0639\u064a\u062f\u0646\u0627 \u0645\u0646 10 \u0635\u0628\u0627\u062d\u064b\u0627 \u0644\u062d\u062f 10 \u0645\u0633\u0627\u0621\u064b\u060c \u0648\u0627\u0644\u062a\u0648\u0635\u064a\u0644 \u062f\u0627\u062e\u0644 \u0627\u0644\u0642\u0627\u0647\u0631\u0629 \u062e\u0644\u0627\u0644 24 \u0633\u0627\u0639\u0629."

    if "\u0627\u0644\u0648\u0642\u062a" in text or "\u0627\u0644\u0633\u0627\u0639\u0629" in text:
        return f"\u0627\u0644\u0648\u0642\u062a \u0627\u0644\u0622\u0646 {datetime.now().strftime('%H:%M')}."

    product = find_product(text)
    if product:
        if "\u0627\u0636\u0641" in text or "\u0627\u0634\u062a\u0631\u064a" in text or "\u0637\u0644\u0628" in text:
            return add_to_cart(product)
        details = PRODUCTS[product]
        return f"{product}: \u0627\u0644\u0633\u0639\u0631 {money(details['price'])}\u060c \u0648\u0627\u0644\u0645\u062a\u0627\u062d {details['stock']}."

    if "\u0627\u0644\u0633\u0644\u0627\u0645" in text or "\u0627\u0647\u0644\u0627" in text:
        return "\u0623\u0647\u0644\u0627 \u0628\u064a\u0643! \u0623\u0646\u0627 \u0645\u0633\u0627\u0639\u062f \u0627\u0644\u0645\u062a\u062c\u0631. \u0627\u0643\u062a\u0628 \u00ab\u0645\u0633\u0627\u0639\u062f\u0629\u00bb \u0644\u0645\u0639\u0631\u0641\u0629 \u0627\u0644\u0623\u0648\u0627\u0645\u0631."

    return "\u0645\u0634 \u0644\u0627\u0642\u064a \u0627\u0644\u0645\u0637\u0644\u0648\u0628. \u0627\u0643\u062a\u0628 \u00ab\u0627\u0644\u0645\u0646\u062a\u062c\u0627\u062a\u00bb \u0623\u0648 \u00ab\u0645\u0633\u0627\u0639\u062f\u0629\u00bb."


def main() -> None:
    print("Chatbot: \u0623\u0647\u0644\u0627 \u0628\u064a\u0643! \u0623\u0646\u0627 \u0645\u0633\u0627\u0639\u062f \u0645\u062a\u062c\u0631 \u0623\u0648\u0641\u0644\u0627\u064a\u0646.")
    while True:
        message = input("\u0623\u0646\u062a: ")
        print(f"Chatbot: {reply(message)}")
        if message.strip().lower() in {"\u062e\u0631\u0648\u062c", "exit", "quit"}:
            break


if __name__ == "__main__":
    main()
