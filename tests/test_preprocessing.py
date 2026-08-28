from preprocessing.text_preprocessor import preprocess_text


def test_normal_text():
    text = "I am feeling really stressed about my workload."
    result = preprocess_text(text)

    print("\nNormal text:")
    print("Original:", text)
    print("Processed:", result)


def test_punctuation():
    text = "I am stressed!!! Really stressed!!!"
    result = preprocess_text(text)

    print("\nPunctuation:")
    print("Original:", text)
    print("Processed:", result)


def test_special_characters():
    text = "I am stressed @#$%^&* today!"
    result = preprocess_text(text)

    print("\nSpecial characters:")
    print("Original:", text)
    print("Processed:", result)


def test_repeated_spaces():
    text = "I    am     feeling       stressed."
    result = preprocess_text(text)

    print("\nRepeated spaces:")
    print("Original:", text)
    print("Processed:", result)


def test_empty_text():
    text = ""
    result = preprocess_text(text)

    print("\nEmpty text:")
    print("Result:", repr(result))


def test_whitespace():
    text = "       "
    result = preprocess_text(text)

    print("\nWhitespace:")
    print("Result:", repr(result))


def test_long_text():
    text = """
    I have been working continuously for several days.
    The workload has become difficult to manage.
    I feel exhausted and unable to concentrate properly.
    """

    result = preprocess_text(text)

    print("\nLong text:")
    print("Processed:", result)


if __name__ == "__main__":
    test_normal_text()
    test_punctuation()
    test_special_characters()
    test_repeated_spaces()
    test_empty_text()
    test_whitespace()
    test_long_text()

def test_lemmatization():
    text = "The employees were working on multiple projects."

    result = preprocess_text(text)

    print("\nLemmatization:")
    print("Original:", text)
    print("Processed:", result)

test_lemmatization()