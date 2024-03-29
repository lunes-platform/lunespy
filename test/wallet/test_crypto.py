from lunespy.crypto import hidden_seed, to_address, to_private_key, to_public_key
from pytest import mark


@mark.parametrize(
    "nonce, seed, hidded_seed",
    [
        (
            0,
            "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
            [163, 66, 17, 225, 21, 144, 128, 203, 241, 21, 205, 209, 16, 138, 219, 155, 50, 48, 24, 209, 227, 79, 35, 104, 252, 102, 213, 74, 63, 165, 20, 96]
        ),
        (
            1,
            "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
            [158, 195, 158, 43, 235, 175, 81, 113, 71, 142, 134, 117, 226, 247, 140, 189, 9, 86, 193, 54, 59, 40, 100, 59, 213, 171, 8, 113, 151, 244, 43, 116]
        ),
        (
            2,
            "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
            [50, 135, 161, 15, 52, 78, 234, 177, 234, 101, 67, 192, 68, 174, 104, 124, 28, 156, 23, 33, 81, 118, 210, 255, 127, 127, 59, 24, 148, 215, 25, 141]
        ),
        (
            3,
            "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
            [68, 188, 249, 142, 153, 123, 119, 187, 134, 139, 142, 224, 144, 233, 96, 219, 118, 79, 3, 179, 172, 145, 191, 189, 235, 205, 232, 119, 176, 55, 76, 197]
        ),
        (
            4,
            "scrub guard swim catch range upon dawn ensure segment alpha sentence spend effort bar benefit",
            [176, 132, 66, 150, 25, 7, 98, 166, 0, 121, 84, 17, 161, 132, 204, 58, 19, 4, 158, 161, 26, 205, 63, 198, 230, 171, 218, 199, 199, 217, 26, 102]
        )
    ]
)
def test_nonce_seed_for_0_1_2_3_4_nonces(nonce: int, seed: str, hidded_seed: list):
    assert hidded_seed == list(hidden_seed(nonce, seed))


@mark.parametrize(
    "hidded_seed, private_key",
    [
        (
            [163, 66, 17, 225, 21, 144, 128, 203, 241, 21, 205, 209, 16, 138, 219, 155, 50, 48, 24, 209, 227, 79, 35, 104, 252, 102, 213, 74, 63, 165, 20, 96],
            [160, 66, 17, 225, 21, 144, 128, 203, 241, 21, 205, 209, 16, 138, 219, 155, 50, 48, 24, 209, 227, 79, 35, 104, 252, 102, 213, 74, 63, 165, 20, 96]
        ),
        (
            [158, 195, 158, 43, 235, 175, 81, 113, 71, 142, 134, 117, 226, 247, 140, 189, 9, 86, 193, 54, 59, 40, 100, 59, 213, 171, 8, 113, 151, 244, 43, 116],
            [152, 195, 158, 43, 235, 175, 81, 113, 71, 142, 134, 117, 226, 247, 140, 189, 9, 86, 193, 54, 59, 40, 100, 59, 213, 171, 8, 113, 151, 244, 43, 116]
        ),
        (
            [50, 135, 161, 15, 52, 78, 234, 177, 234, 101, 67, 192, 68, 174, 104, 124, 28, 156, 23, 33, 81, 118, 210, 255, 127, 127, 59, 24, 148, 215, 25, 141],
            [48, 135, 161, 15, 52, 78, 234, 177, 234, 101, 67, 192, 68, 174, 104, 124, 28, 156, 23, 33, 81, 118, 210, 255, 127, 127, 59, 24, 148, 215, 25, 77]
        ),
        (
            [68, 188, 249, 142, 153, 123, 119, 187, 134, 139, 142, 224, 144, 233, 96, 219, 118, 79, 3, 179, 172, 145, 191, 189, 235, 205, 232, 119, 176, 55, 76, 197],
            [64, 188, 249, 142, 153, 123, 119, 187, 134, 139, 142, 224, 144, 233, 96, 219, 118, 79, 3, 179, 172, 145, 191, 189, 235, 205, 232, 119, 176, 55, 76, 69]
        ),
        (
            [176, 132, 66, 150, 25, 7, 98, 166, 0, 121, 84, 17, 161, 132, 204, 58, 19, 4, 158, 161, 26, 205, 63, 198, 230, 171, 218, 199, 199, 217, 26, 102],
            [176, 132, 66, 150, 25, 7, 98, 166, 0, 121, 84, 17, 161, 132, 204, 58, 19, 4, 158, 161, 26, 205, 63, 198, 230, 171, 218, 199, 199, 217, 26, 102]
        )
    ]
)
def test_raw_seed_for_0_1_2_3_4_nonces(hidded_seed, private_key):

    assert private_key == list(to_private_key(bytes(hidded_seed)))


@mark.parametrize(
    "private_key, public_key",
    [
        (
            [160, 66, 17, 225, 21, 144, 128, 203, 241, 21, 205, 209, 16, 138, 219, 155, 50, 48, 24, 209, 227, 79, 35, 104, 252, 102, 213, 74, 63, 165, 20, 96],
            [28, 105, 36, 199, 36, 111, 120, 95, 152, 208, 215, 39, 161, 71, 78, 237, 200, 160, 71, 209, 177, 102, 140, 170, 56, 206, 9, 214, 227, 38, 117, 117]
        ),
        (
            [152, 195, 158, 43, 235, 175, 81, 113, 71, 142, 134, 117, 226, 247, 140, 189, 9, 86, 193, 54, 59, 40, 100, 59, 213, 171, 8, 113, 151, 244, 43, 116],
            [138, 251, 177, 135, 204, 17, 215, 139, 107, 110, 163, 159, 69, 66, 230, 125, 46, 90, 155, 251, 112, 76, 80, 226, 246, 159, 0, 247, 24, 204, 238, 127]
        ),
        (
            [48, 135, 161, 15, 52, 78, 234, 177, 234, 101, 67, 192, 68, 174, 104, 124, 28, 156, 23, 33, 81, 118, 210, 255, 127, 127, 59, 24, 148, 215, 25, 77],
            [83, 143, 55, 207, 188, 113, 76, 98, 188, 187, 21, 6, 121, 237, 114, 87, 56, 119, 247, 123, 107, 235, 127, 93, 111, 125, 177, 254, 234, 7, 182, 102]
        ),
        (
            [64, 188, 249, 142, 153, 123, 119, 187, 134, 139, 142, 224, 144, 233, 96, 219, 118, 79, 3, 179, 172, 145, 191, 189, 235, 205, 232, 119, 176, 55, 76, 69],
            [24, 17, 29, 210, 50, 221, 206, 124, 241, 169, 109, 116, 202, 228, 241, 10, 66, 235, 31, 179, 74, 61, 220, 114, 110, 17, 25, 9, 161, 78, 24, 115]
        ),
        (
            [176, 132, 66, 150, 25, 7, 98, 166, 0, 121, 84, 17, 161, 132, 204, 58, 19, 4, 158, 161, 26, 205, 63, 198, 230, 171, 218, 199, 199, 217, 26, 102],
            [199, 51, 26, 241, 231, 42, 46, 169, 1, 155, 227, 85, 160, 76, 123, 191, 181, 159, 48, 66, 209, 156, 162, 79, 235, 66, 199, 211, 35, 21, 161, 56]
        )
    ]
)
def test_hash_seed_for_0_1_2_3_4_nonces(private_key: list, public_key: list):
    assert public_key == list(to_public_key(bytes(private_key)))


@mark.parametrize(
    "public_key, address_mainnet",
    [
        (
            [28, 105, 36, 199, 36, 111, 120, 95, 152, 208, 215, 39, 161, 71, 78, 237, 200, 160, 71, 209, 177, 102, 140, 170, 56, 206, 9, 214, 227, 38, 117, 117],
            [1, 49, 44, 46, 82, 88, 220, 91, 204, 187, 92, 83, 89, 68, 39, 15, 115, 185, 143, 151, 57, 38, 99, 41, 200, 192]
        ),
        (
            [138, 251, 177, 135, 204, 17, 215, 139, 107, 110, 163, 159, 69, 66, 230, 125, 46, 90, 155, 251, 112, 76, 80, 226, 246, 159, 0, 247, 24, 204, 238, 127],
            [1, 49, 100, 15, 35, 15, 57, 108, 76, 243, 246, 206, 122, 97, 86, 56, 125, 82, 146, 153, 2, 191, 247, 116, 35, 216]
        ),
        (
            [83, 143, 55, 207, 188, 113, 76, 98, 188, 187, 21, 6, 121, 237, 114, 87, 56, 119, 247, 123, 107, 235, 127, 93, 111, 125, 177, 254, 234, 7, 182, 102],
            [1, 49, 70, 204, 18, 41, 121, 119, 51, 99, 11, 250, 56, 190, 114, 202, 109, 245, 133, 232, 82, 31, 212, 75, 87, 56]
        ),
        (
            [24, 17, 29, 210, 50, 221, 206, 124, 241, 169, 109, 116, 202, 228, 241, 10, 66, 235, 31, 179, 74, 61, 220, 114, 110, 17, 25, 9, 161, 78, 24, 115],
            [1, 49, 132, 46, 58, 18, 143, 212, 98, 181, 24, 5, 121, 141, 54, 144, 157, 172, 120, 255, 157, 67, 171, 180, 211, 179]
        ),
        (
            [199, 51, 26, 241, 231, 42, 46, 169, 1, 155, 227, 85, 160, 76, 123, 191, 181, 159, 48, 66, 209, 156, 162, 79, 235, 66, 199, 211, 35, 21, 161, 56],
            [1, 49, 125, 33, 20, 80, 131, 75, 252, 110, 0, 36, 84, 146, 24, 131, 61, 235, 243, 119, 150, 138, 78, 202, 75, 45]
        )
    ]
)
def test_generate_private_key_for_0_1_2_3_4_nonces(public_key, address_mainnet):
    assert address_mainnet == list(to_address(public_key=bytes(public_key), chain=1, addr_version=1))


@mark.parametrize(
    "public_key, address_testnet",
    [
        (
            [28, 105, 36, 199, 36, 111, 120, 95, 152, 208, 215, 39, 161, 71, 78, 237, 200, 160, 71, 209, 177, 102, 140, 170, 56, 206, 9, 214, 227, 38, 117, 117],
            [1, 48, 44, 46, 82, 88, 220, 91, 204, 187, 92, 83, 89, 68, 39, 15, 115, 185, 143, 151, 57, 38, 209, 43, 93, 192]
        ),
        (
            [138, 251, 177, 135, 204, 17, 215, 139, 107, 110, 163, 159, 69, 66, 230, 125, 46, 90, 155, 251, 112, 76, 80, 226, 246, 159, 0, 247, 24, 204, 238, 127],
            [1, 48, 100, 15, 35, 15, 57, 108, 76, 243, 246, 206, 122, 97, 86, 56, 125, 82, 146, 153, 2, 191, 220, 25, 203, 2]
        ),
        (
            [83, 143, 55, 207, 188, 113, 76, 98, 188, 187, 21, 6, 121, 237, 114, 87, 56, 119, 247, 123, 107, 235, 127, 93, 111, 125, 177, 254, 234, 7, 182, 102],
            [1, 48, 70, 204, 18, 41, 121, 119, 51, 99, 11, 250, 56, 190, 114, 202, 109, 245, 133, 232, 82, 31, 66, 65, 70, 16]
        ),
        (
            [24, 17, 29, 210, 50, 221, 206, 124, 241, 169, 109, 116, 202, 228, 241, 10, 66, 235, 31, 179, 74, 61, 220, 114, 110, 17, 25, 9, 161, 78, 24, 115],
            [1, 48, 132, 46, 58, 18, 143, 212, 98, 181, 24, 5, 121, 141, 54, 144, 157, 172, 120, 255, 157, 67, 230, 111, 30, 167]
        ),
        (
            [199, 51, 26, 241, 231, 42, 46, 169, 1, 155, 227, 85, 160, 76, 123, 191, 181, 159, 48, 66, 209, 156, 162, 79, 235, 66, 199, 211, 35, 21, 161, 56],
            [1, 48, 125, 33, 20, 80, 131, 75, 252, 110, 0, 36, 84, 146, 24, 131, 61, 235, 243, 119, 150, 138, 150, 25, 182, 187]
        )
    ]
)
def test_generate_private_key_for_0_1_2_3_4_nonces(public_key, address_testnet):
    assert address_testnet == list(to_address(public_key=bytes(public_key), chain=0, addr_version=1))
