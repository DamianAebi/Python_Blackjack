import random

from Utils.one_thousand_words import words


class Utils:

    def __init__(self):
        pass

    @staticmethod
    def validated_input(input_string: str, validation_type):
        while True:
            user_input = input(input_string)
            try:
                validation_type(user_input)
            except ValueError:
                print("Input invalid. Please enter a ", validation_type)
                continue

            break

        return validation_type(user_input)

    @staticmethod
    def generate_random_numbers(amount: int) -> list[int]:
        list_of_random_numbers = []
        for i in range(amount):
            random_number = random.randint(1, amount)
            list_of_random_numbers.append(random_number)

        return list_of_random_numbers

    @staticmethod
    def generate_random_words(amount: int) -> list[str]:
        list_of_random_words = []
        for i in range(amount):
            random_word = random.choice(words)
            list_of_random_words.append(random_word)

        return list_of_random_words

    @staticmethod
    def get_key_from_value(d, val):
        keys = [k for k, v in d.items() if v == val]
        if keys:
            return keys[0]
        return None
