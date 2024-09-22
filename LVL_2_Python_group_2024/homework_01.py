text = input("Введіть рядок: ")


cleaned_text = text.replace(' ', '')


if cleaned_text == cleaned_text:
    print("Це паліндром!")
else:
    print("Це не паліндром.")

