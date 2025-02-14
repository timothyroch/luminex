import unittest
from cryptocurrency.wallet.key_management.key_generator import KeyGenerator
from cryptocurrency.wallet.key_management.key_storage import KeyStorage
from cryptocurrency.wallet.key_management.key_recovery import KeyRecovery

class TestKeyManagement(unittest.TestCase):
    def setUp(self):
        """
        Set up the environment for testing key management.
        """
        self.key_generator = KeyGenerator()
        self.key_storage = KeyStorage(storage_path="test_key_storage.json")
        self.key_recovery = KeyRecovery()

        # Generate test keys
        self.private_key, self.public_key = self.key_generator.generate_key_pair()
        self.address = self.key_generator.get_address(self.public_key)
        self.seed_phrase = self.key_recovery.generate_seed_phrase()

    def tearDown(self):
        """
        Clean up after tests by removing the test key storage file.
        """
        import os
        if os.path.exists("test_key_storage.json"):
            os.remove("test_key_storage.json")

    def test_key_generation(self):
        """
        Test that a valid key pair is generated.
        """
        private_key, public_key = self.key_generator.generate_key_pair()
        self.assertIsNotNone(private_key, "Private key generation failed")
        self.assertIsNotNone(public_key, "Public key generation failed")
        print("Key generation test passed.")

    def test_key_storage(self):
        """
        Test that keys can be stored and retrieved securely.
        """
        self.key_storage.store_key(self.address, self.private_key)
        retrieved_key = self.key_storage.get_key(self.address)
        self.assertEqual(retrieved_key, self.private_key, "Retrieved private key does not match stored key")
        print("Key storage test passed.")

    def test_key_recovery(self):
        """
        Test that a seed phrase can recover the correct key pair.
        """
        recovered_private_key, recovered_public_key = self.key_recovery.recover_key_pair(self.seed_phrase)
        self.assertIsNotNone(recovered_private_key, "Private key recovery failed")
        self.assertIsNotNone(recovered_public_key, "Public key recovery failed")
        print("Key recovery test passed.")

    def test_invalid_key_retrieval(self):
        """
        Test that retrieving a key for a non-existent address raises an error.
        """
        with self.assertRaises(KeyError):
            self.key_storage.get_key("invalid_address")
        print("Invalid key retrieval test passed.")

    def test_invalid_seed_phrase(self):
        """
        Test that an invalid seed phrase does not recover a key pair.
        """
        invalid_seed = "invalid seed phrase"
        with self.assertRaises(ValueError):
            self.key_recovery.recover_key_pair(invalid_seed)
        print("Invalid seed phrase test passed.")

if __name__ == "__main__":
    unittest.main()
