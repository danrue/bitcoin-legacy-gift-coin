from coin_lib import BitcoinWallet
from bitcoinlib.keys import HDKey


class TestBitcoinWallet:
    def test_generate_seed_phrase(self):
        seed_phrase = BitcoinWallet.generate_seed_phrase()
        assert seed_phrase is not None
        assert isinstance(seed_phrase, str)
        assert len(seed_phrase.split()) == 12

    def test_create_wallet(self):
        seed_phrase = BitcoinWallet.generate_seed_phrase()
        wallet = BitcoinWallet.create_wallet(seed_phrase)
        assert wallet is not None
        assert isinstance(wallet, HDKey)

    def test_get_address(self):
        seed_phrase = BitcoinWallet.generate_seed_phrase()
        wallet = BitcoinWallet.create_wallet(seed_phrase)
        address = BitcoinWallet.get_address(wallet)
        assert address is not None
        assert isinstance(address, str)
        assert address.startswith("bc1")

    def test_init_with_seed_phrase(self):
        seed_phrase = BitcoinWallet.generate_seed_phrase()
        wallet = BitcoinWallet(seed_phrase)
        assert wallet.seed_phrase == seed_phrase
        assert wallet.wallet is not None
        assert wallet.address is not None

    def test_init_without_seed_phrase(self):
        wallet = BitcoinWallet()
        assert wallet.seed_phrase is not None
        assert wallet.wallet is not None
        assert wallet.address is not None
