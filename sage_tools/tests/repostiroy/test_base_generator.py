from unittest.mock import patch, MagicMock, Mock
from datetime import datetime, timezone
from django.utils.timezone import make_aware


class TestBaseDataGenerator:
    """Test suite for the `BaseDataGenerator` class."""

    def test_create_placeholder_image(self, generator):
        img_data, filename, format = generator.create_placeholder_image(
            1, "test_subject"
        )
        assert filename == "test_subject_1_440x660.webp"
        assert format == "WEBP"
        assert isinstance(img_data, bytes)

    def test_get_random_secret(self, generator):
        secret = generator.get_random_secret(10)
        assert isinstance(secret, str)
        assert len(secret) > 0

    def test_get_random_words(self, generator):
        words = generator.get_random_words(3)
        assert isinstance(words, str)
        assert len(words.split()) == 3

    def test_get_random_color(self, generator):
        color = generator.get_random_color()
        assert isinstance(color, str)
        assert len(color) > 0

    def test_get_random_int(self, generator):
        random_int = generator.get_random_int(1, 10)
        assert 1 <= random_int <= 10

    def test_get_random_hex_code(self, generator):
        hex_code = generator.get_random_hex_code()
        assert isinstance(hex_code, str)
        assert hex_code.startswith("#")

    def test_get_random_time(self, generator):
        random_time = generator.get_random_time()
        assert random_time is not None

    def test_get_random_datetime(self, generator):
        start = make_aware(datetime(2020, 1, 1))
        end = make_aware(datetime(2020, 12, 31))
        random_datetime = generator.get_random_datetime(start=start, end=end)
        assert start <= random_datetime <= end

    def test_get_random_boolean(self, generator):
        random_bool = generator.get_random_boolean()
        assert isinstance(random_bool, bool)

    def test_get_random_booleans(self, generator):
        booleans = generator.get_random_booleans(total_true=2, total_false=3)
        assert booleans.count(True) == 2
        assert booleans.count(False) == 3

    def test_get_random_population(self, generator):
        population = [1, 2, 3, 4, 5]
        selected, remaining = generator.get_random_population(population, 2)
        assert len(selected) == 2
        assert len(remaining) == 3
        assert set(selected).union(set(remaining)) == set(population)

    def test_get_random_object(self, generator):
        population = [1, 2, 3, 4, 5]
        selected = generator.get_random_object(population)
        assert selected in population

    def test_get_random_float(self, generator):
        random_float = generator.get_random_float(1.0, 10.0)
        assert 1.0 <= random_float <= 10.0

    def test_get_random_currency(self, generator):
        currency = generator.get_random_currency()
        assert currency in ["IRR", "USD", "EUR"]

    def test_get_random_price(self, generator):
        price = generator.get_random_price()
        assert isinstance(price, float)
        assert price > 0

    def test_get_random_number(self, generator):
        random_number = generator.get_random_number()
        assert -100 <= random_number <= 1000

    def test_get_random_County_code(self, generator):
        county_code = generator.get_random_County_code()
        assert isinstance(county_code, str)
        assert len(county_code) == 2

    def test_get_random_city(self, generator):
        city = generator.get_random_city()
        assert isinstance(city, str)
        assert len(city) > 0

    def test_get_random_address(self, generator):
        address = generator.get_random_address()
        assert isinstance(address, str)
        assert len(address) > 0

    def test_get_random_postal_code(self, generator):
        postal_code = generator.get_random_postal_code()
        assert isinstance(postal_code, str)
        assert len(postal_code) > 0

    def test_get_random_street_number(self, generator):
        street_number = generator.get_random_street_number()
        assert isinstance(street_number, str)
        assert len(street_number) > 0

    def test_get_random_full_name(self, generator):
        full_name = generator.get_random_full_name()
        assert isinstance(full_name, str)
        assert len(full_name.split()) >= 2

    def test_get_random_first_name(self, generator):
        first_name = generator.get_random_first_name()
        assert isinstance(first_name, str)
        assert len(first_name) > 0

    def test_get_random_last_name(self, generator):
        last_name = generator.get_random_last_name()
        assert isinstance(last_name, str)
        assert len(last_name) > 0

    def test_get_random_telephone(self, generator):
        telephone = generator.get_random_telephone()
        assert isinstance(telephone, str)
        assert len(telephone) > 0

    def test_get_random_status(self, generator):
        status = generator.get_random_status()
        assert status in [
            "waiting",
            "expiring",
            "cancelled",
            "shipped",
            "processing",
            "delivered",
            "completed",
        ]

    def test_get_image_banner(self, generator):
        banner = generator.get_image_banner(0)
        assert banner == "first"

        banner = generator.get_image_banner(1)
        assert banner == "second"

        banner = generator.get_image_banner(2)
        assert banner == "other"

    def test_get_random_image(self, generator):
        image = generator.get_random_image(1)
        assert image == "first"

        image = generator.get_random_image(2)
        assert image == "second"

        image = generator.get_random_image(3)
        assert image == "other"

    def test_get_random_sentence(self, generator):
        sentence = generator.get_random_sentence()
        assert isinstance(sentence, str)
        assert len(sentence) > 0

    def test_get_random_email(self, generator):
        email = generator.get_random_email()
        assert isinstance(email, str)
        assert "@" in email

    def test_get_random_job(self, generator):
        job = generator.get_random_job()
        assert isinstance(job, str)
        assert len(job) > 0

    def test_get_random_gender(self, generator):
        gender = generator.get_random_gender()
        assert gender in ["male", "female"]

    def test_get_random_province(self, generator):
        province = generator.get_random_province()
        assert isinstance(province, str)
        assert len(province) > 0

    def test_get_unique_phone_number_set(self, generator):
        phone_numbers = generator.get_unique_phone_number_set(min_length=5, digits=7)
        assert isinstance(phone_numbers, set)
        assert len(phone_numbers) >= 5
        assert all(len(phone) == 7 for phone in phone_numbers)

    def test_get_currency_exchange(self, generator):
        value = generator.get_currency_exchange(
            "USD", 100, (1.0, 1.5), (2.0, 3.0), (0.8, 1.2)
        )
        assert isinstance(value, (int, float))

    def test_get_voucher_kind(self, generator):
        kind = generator.get_voucher_kind()
        assert kind in ["static_based", "code_based"]

    def test_get_voucher_type(self, generator):
        voucher_type = generator.get_voucher_type()
        assert voucher_type in ["fixed_price_based", "percentage_based"]

    def test_get_voucher_status(self, generator):
        status = generator.get_voucher_status()
        assert status in ["open", "suspend", "consumed"]

    def test_get_random_percentage(self, generator):
        percentage = generator.get_random_percentage(10, 50)
        assert 10 <= percentage <= 50

    def test_get_unique_hashes_list(self, generator):
        total = 5
        element_length = 12
        hashes = generator.get_unique_hashes_list(
            total=total, element_length=element_length
        )
        assert isinstance(hashes, list)
        assert len(hashes) == total
        assert len(hashes) == len(set(hashes))

    def test_get_random_time_between_two_datetime_objects(self, generator):
        start_time = datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        end_time = datetime(2021, 1, 1, 23, 59, 59, tzinfo=timezone.utc)
        random_time = generator.get_random_time_between_two_datetime_objects(
            start_time, end_time
        )
        assert start_time <= random_time <= end_time

    def test_get_random_spice(self, generator):
        spice = generator.get_random_spice()
        assert isinstance(spice, str)
        assert len(spice) > 0

    @patch("django.db.models.Model")
    def test_add_to_m2m(self, mock_model, generator):
        mock_objs = [Mock(), Mock(), Mock()]
        mock_attr = MagicMock()
        mock_model.some_field = mock_attr

        generator.add_to_m2m(
            objs=mock_objs, target_field="some_field", item_pre_obj=2, item=mock_model
        )

        assert mock_attr.add.called
        assert mock_attr.add.call_count == 1
