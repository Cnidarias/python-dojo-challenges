def encrypt(text, key, join=True):
    """
    Encrypts a text with the rail cipher method using the specified key

    The rail fence cipher works by writing the text into a grid with `key` rows
    using a zig zag pattern and then reading the result line by line

    Encrypting the text "Hello World!" with key 3 looks like this
    H - - - o - - - r - - -
    - e - l -   - o - l - !
    - - l - - - W - - - d -

    Read from top to bottom yields:
    "Horel ol!lWd"

    :param text: The text you want to encrypt
    :param key: The key to use for the cipher
    :param join: Should the result be joined together - if not a list is returned with the elements in order
    :return: The encrypted text either joined together or as a list of elements
    """
    rail = [[] for _ in range(key)]
    current_rail_idx = 0
    current_rail_direction = -1

    for c in text:
        if current_rail_idx == 0 or current_rail_idx == key - 1:
            current_rail_direction = -current_rail_direction
        rail[current_rail_idx].append(c)
        current_rail_idx += current_rail_direction
    flat_list = [item for r in rail for item in r]
    return "".join(flat_list) if join else flat_list


def decrypt(text, key, join=True):
    """
    Decrypts a text with  the rail cipher method using the `key` for the number of rows

    The rail fence cipher works by writing the text into a grid with `key` rows
    using a zig zag pattern and then reading the result line by line

    Decrypting such a text means that you create the zig-zag pattern and then
    write the encoded text into that pattern line by line

    Using the text "Horel ol!lWd" as an example:

    pattern:
    * - - - * - - - * - - -
    - * - * - * - * - * - *
    - - * - - - * - - - * -

    filled in:
    H - - - o - - - r - - -
    - e - l -   - o - l - !
    - - l - - - W - - - d -

    Read in the zig-zag pattern yields
    "Hello World!"

    :param text: The encrypted text
    :param key: The key used in the cipher
    :param join: Should the result be joined together - if not a list is returned with the elements in order
    :return: The decrypted text either joined together or as a list of elements
    """
    jumbled_indices = encrypt(range(len(text)), key, join=False)
    plain_text_list = [c for _, c in sorted(zip(jumbled_indices, text))]
    return "".join(plain_text_list) if join else plain_text_list


if __name__ == '__main__':
    test_text = "Hello World!"
    for i in range(2, 10, 1):
        encrypted = encrypt(test_text, i)
        decrypted = decrypt(encrypted, i)
        assert decrypted == test_text
        print(f"{i} {encrypted} => {decrypted}")
