"""Test rc_cipher behaviour."""
import unittest

import faker

from common.utils import rc_cipher


class TestCase(unittest.TestCase):
    """Test rc_cipher behaviour."""

    def test_encode(self):
        """Check the string is correctly encoded."""
        self.assertEqual(rc_cipher.encode("hellopass123"), "myFWAmp5suE6bODn")

    def test_decode(self):
        """Check the encoded string is correctly decoded."""
        self.assertEqual(rc_cipher.decode("myFWAmp5suE6bODn"), "hellopass123")

    def test_decode_encoded(self):
        """Check decoding an encoded string matches the original."""
        fake = faker.Faker()
        for _ in range(10):
            string = fake.password(length=15)
            with self.subTest(string=string):
                encoded = rc_cipher.encode(string)
                self.assertNotEqual(string, encoded)
                self.assertEqual(string, rc_cipher.decode(encoded))
