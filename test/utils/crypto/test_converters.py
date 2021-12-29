
from lunespy.utils.crypto.converters import bits_to_bytes
from lunespy.utils.crypto.converters import string_to_list
from lunespy.utils.crypto.converters import bytes_to_string
from lunespy.utils.crypto.converters import string_to_bytes
from lunespy.utils.crypto.converters import sha256
from lunespy.utils.crypto.converters import hash_data
from pytest import mark


@mark.parametrize(
    "input, output",
    [(101, 13.5), (1, 1), (11, 2.25), (103, 13.75), (1011, 127.25)]
)
def test_function_bits_to_bytes_with_multiple_input(input, output):
    assert bits_to_bytes(input) == output


@mark.parametrize(
    "input, output",
    [
        ("lunes", b"lunes"),
        ("blockchain", b"blockchain"),
        ("1234567890", b"1234567890"),
        ("``#@$%#%V%C#$%@$@$", b"``#@$%#%V%C#$%@$@$")
    ]
)
def test_function_string_to_bytes_with_multiple_string_should_be_return_bytes(input, output):
    assert string_to_bytes(input) == output


@mark.parametrize(
     "input, output",
     [
        ([112, 90, 45, 3], "pZ-\x03"),
        ([1, 2, 3, 4], "\x01\x02\x03\x04"),
        ([100, 200, 300, 400], "dÈĬƐ"),
        ([1000, 2000, 3000, 4000], "Ϩߐஸྠ"),
        ([50, 9, 70, 30], "2\tF\x1e")
     ]
)
def test_function_bytes_to_string_with_multiple_list_of_4_int_should_be_return_string(input, output):
    assert bytes_to_string(input) == output


@mark.parametrize(
    "input, output",
    [
        (b"1234", "\x00\r\x9b"),
        (b"chain", "\x18\x14z\x8b"),
        (b"LUNES", '\r"Qg'),
        (b"bLockchain", "\x03\x8a6¿CÊ\x81+")
    ]
)
def test_function_bytes_to_string_with_multiple_bytes_string_should_be_return_string(input, output):
    assert bytes_to_string(input, True) == output


@mark.parametrize(
    "nonce,output",
    [
        (
            0,
            [143, 196, 47, 113, 246, 40, 163, 0, 200, 218, 161, 254, 70, 68, 236, 106, 145, 138, 209, 254, 96, 236, 55, 11, 201, 75, 140, 165, 3, 147, 132, 124]
        ),
        (
            1,
            [175, 212, 243, 73, 2, 47, 142, 121, 28, 225, 79, 206, 27, 183, 76, 99, 97, 45, 229, 93, 169, 179, 247, 174, 45, 55, 247, 237, 169, 151, 62, 219]
        ),
        (
            2,
            [74, 155, 255, 114, 251, 90, 49, 14, 52, 236, 27, 138, 107, 247, 31, 10, 72, 97, 15, 115, 169, 36, 181, 233, 75, 109, 225, 186, 173, 35, 252, 101]
        ),
    ]
)
def test_hash_data_multiple_nonce_should_be_return_hash_seed_list_of_int(nonce, output):
    from struct import pack
    seed = "sausage say arrive tackle color melody answer tobacco garlic smoke cereal fade"
    seed_hash = hash_data(pack(">L", nonce) + string_to_bytes(seed))
    assert seed_hash == bytes_to_string(output)


@mark.parametrize(
    "seed, output",
    [
        (
            "segment bridge lady radar gravity ozone tourist lucky rug betray mix stand",
            [106, 241, 96, 6, 213, 44, 127, 57, 245, 6, 216, 155, 39, 101, 25, 175, 54, 131, 225, 195, 71, 238, 132, 27, 120, 165, 231, 93, 254, 196, 113, 42]
        ),
        (
            "hair receive trash tomato cinnamon frequent clinic absorb air clay hungry receive",
            [125, 254, 88, 238, 164, 119, 242, 14, 3, 86, 162, 211, 134, 69, 74, 24, 46, 7, 88, 60, 132, 89, 64, 128, 133, 233, 194, 92, 63, 135, 210, 190]
        ),
        (
            "donkey tone age survey cram lunch midnight hint rotate idle forget share",
            [89, 43, 64, 181, 219, 245, 62, 211, 28, 146, 17, 142, 205, 220, 215, 156, 249, 60, 175, 189, 91, 174, 128, 25, 245, 84, 62, 16, 177, 196, 171, 236]
        ),
        (
            "marriage robot wire again cluster giraffe will brave excuse imitate guitar invest",
            [116, 228, 131, 31, 13, 104, 107, 177, 220, 187, 186, 226, 219, 45, 76, 247, 248, 89, 81, 196, 231, 16, 97, 245, 243, 195, 178, 46, 166, 72, 140, 37]
        ),
        (
            "crime orphan prize main predict asset method raise can mountain ten envelope",
            [50, 30, 12, 210, 168, 243, 251, 190, 187, 91, 129, 179, 156, 122, 90, 24, 206, 86, 224, 44, 233, 170, 123, 131, 63, 27, 25, 207, 163, 120, 2, 184]
        )
    ]
)
def test_function_hash_data_multiple_seed_should_be_return_hash_seed_list_of_int(seed, output):
    from struct import pack
    nonce = 0
    seed_hash = hash_data(pack(">L", nonce) + string_to_bytes(seed))

    assert seed_hash == bytes_to_string(output)


@mark.parametrize(
    "input, output",
    [
        (
            "lunes",
            [96, 32, 172, 151, 80, 137, 122, 38, 120, 214, 105, 227, 235, 137, 117, 62, 222, 67, 243, 210, 135, 254, 198, 116, 247, 22, 124, 125, 187, 204, 121, 36]
        ),
        (
            "blockchain",
            [239, 119, 151, 225, 61, 58, 117, 82, 105, 70, 163, 188, 240, 13, 174, 201, 252, 156, 156, 77, 81, 221, 199, 204, 93, 248, 136, 247, 77, 212, 52, 209]
        ),
        (
            "0123456789",
            [132, 216, 152, 119, 240, 212, 4, 30, 251, 107, 249, 26, 22, 240, 36, 143, 47, 213, 115, 230, 175, 5, 193, 159, 150, 190, 219, 159, 136, 47, 120, 130]
        ),
        (
            "ABCDEF1235",
            [136, 209, 73, 120, 74, 246, 23, 245, 178, 29, 205, 132, 220, 137, 158, 61, 97, 136, 41, 123, 98, 102, 179, 219, 91, 136, 241, 81, 34, 29, 25, 143]
        ),
        (
            "ffaaff",
            [185, 2, 50, 85, 134, 253, 4, 42, 127, 169, 128, 42, 231, 6, 148, 8, 234, 13, 118, 26, 246, 75, 170, 76, 229, 8, 154, 219, 231, 169, 214, 251]
        ),
    ]
)
def test_function_sha256(input, output):
    print(string_to_list(sha256(input)))
    assert  string_to_list(sha256(input)) == output

