import io
import random
import secrets
from datetime import datetime, timezone
from typing import Any, List, Set, Type, TypeVar

from django.db.models import Model
from django.utils.text import slugify
from django.utils.timezone import make_aware

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    raise ImportError(  # noqa: B904
        "Install `pillow` package. Run `pip install pillow`."
    )

try:
    from mimesis import Address, Datetime, Finance, Food, Numeric, Person, Text
    from mimesis.locales import Locale
except ImportError:
    raise ImportError(  # noqa: B904
        "Install `mimesis` package. Run `pip install mimesis`."
    )

T = TypeVar("T", bound=Model)


class BaseDataGenerator:
    """Generate reusable data."""

    def __init__(self, locale="en"):
        self.person = Person(getattr(Locale, locale.upper()))
        self.text = Text(getattr(Locale, locale.upper()))
        self.fiance = Finance(getattr(Locale, locale.upper()))
        self.address = Address(getattr(Locale, locale.upper()))
        # self.internet = Internet(getattr(Locale, locale.upper()))

    def create_placeholder_image(
        self,
        number: int,
        subject: str,
        size: tuple[int, int] = (440, 660),
        pic_format: str = "WEBP",
    ):
        """Create a gray placeholder image with a number in a specified format.

        Default format is WEBP.

        """
        SUPPORTED_FORMATS = ["JPEG", "PNG", "WEBP"]
        desired_format = pic_format.upper()
        if desired_format not in SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported format: {desired_format}. Supported formats are: {', '.join(SUPPORTED_FORMATS)}"
            )

        light_gray_color = (216, 216, 216)
        image = Image.new("RGB", size, color=light_gray_color)
        draw = ImageDraw.Draw(image)
        font_size = 20  # Adjust as needed
        font = ImageFont.load_default()

        # Prepare the text
        number_text = f"Pic {number}"
        dimension_text = f"{size[0]} x {size[1]}"

        # Manual estimation of text size
        approx_char_width = font_size * 0.6  # Approximation for character width
        number_text_width = approx_char_width * len(number_text)
        dimension_text_width = approx_char_width * len(dimension_text)
        text_height = font_size  # Approximation for text height

        # Calculate positions
        number_text_x = (size[0] - number_text_width) / 2
        number_text_y = (size[1] - text_height) / 2 - 10

        dimension_text_x = (size[0] - dimension_text_width) / 2
        dimension_text_y = number_text_y + text_height + 5

        # Draw the texts
        draw.text((number_text_x, number_text_y), number_text, font=font, fill="black")
        draw.text(
            (dimension_text_x, dimension_text_y),
            dimension_text,
            font=font,
            fill="black",
        )

        # Save the image to a bytes object
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format=desired_format)
        img_byte_arr = img_byte_arr.getvalue()

        width, height = size
        filename = f"{subject}_{number}_{width}x{height}.{desired_format.lower()}"

        return img_byte_arr, filename, desired_format

    def get_random_secret(self, nbytes=20):
        """Generate random string."""
        return secrets.token_urlsafe(nbytes)

    def get_random_words(self, quantity):
        return " ".join(self.text.words(quantity=quantity))

    def get_random_color(self):
        """Generate random code."""
        return Text().color()

    def get_random_int(self, start: int, end: int) -> int:
        return random.randint(start, end)

    def get_random_hex_code(self):
        """Generate random hex code."""
        return Text().hex_color()

    def get_random_time(self):
        """Generate random time."""
        return Datetime().time()

    def get_random_datetime(self, start=None, end=None):
        """Generate a random time between start and end."""
        if start is None:
            current_year = datetime.now().year
            start = make_aware(datetime(current_year, 1, 1))

        if end is None:
            current_year = timezone.now().year
            end = make_aware(datetime(current_year, 12, 31))

        start_timestamp = start.timestamp()
        end_timestamp = end.timestamp()
        random_timestamp = random.uniform(start_timestamp, end_timestamp)
        random_datetime = make_aware(datetime.fromtimestamp(random_timestamp))
        return random_datetime

    def get_random_boolean(self):
        """Generate a random boolean."""
        return random.choice([True, False])

    def get_random_booleans(self, total_true=1, total_false=1, is_shuffle=False):
        trues = [True] * total_true
        falses = [False] * total_false
        total_booleans = trues + falses
        shuffle_booleans = total_booleans[:]
        random.shuffle(shuffle_booleans)
        booleans = shuffle_booleans if is_shuffle else total_booleans
        return booleans

    def get_random_population(self, population, k):
        objs = set(random.sample(population, k))
        population = set(population)
        return list(objs), list(population - objs)

    def get_random_object(self, population):
        return random.choice(population)

    def get_random_float(self, lower, upper):
        """Generate a random float with 2 digits after seperator."""
        return round(random.uniform(lower, upper), 2)

    def get_random_currency(self):
        """Generate a random currency."""
        return random.choice(["IRR", "USD", "EUR"])

    def get_random_price(self):
        """Generate a random price."""
        return Finance().price()

    def get_random_number(self, start=-100, stop=1000):
        """Generate a random number."""
        return Numeric().integer_number(start=start, end=stop)

    def get_random_County_code(self):
        """Generate a random County code."""
        return Address().country_code()

    def get_random_city(self):
        """Generate a random city."""
        return Address().city()

    def get_random_address(self):
        """Generate a random address."""
        return Address().address()

    def get_random_postal_code(self):
        """Generate a random postal_code."""
        return Address().postal_code()

    def get_random_street_number(self):
        """Generate a random street_number."""
        return Address().street_number()

    def get_random_full_name(self):
        """Generate a random full_name."""
        return Person().full_name()

    def get_random_first_name(self):
        return Person().first_name()

    def get_random_last_name(self):
        return Person().last_name()

    def get_random_telephone(self):
        """Generate a random telephone."""
        return slugify(Person().telephone())

    def get_random_status(self):
        """Generate a random status."""
        status = [
            "waiting",
            "expiring",
            "cancelled",
            "shipped",
            "processing",
            "delivered",
            "completed",
        ]
        return random.choice(status)

    def get_image_banner(self, index):
        """Generate a random image banner."""
        if index == 0:
            result = "first"
        elif index == 1:
            result = "second"
        else:
            result = "other"
        return result

    def get_random_image(self, order):
        """Generate a random image choice."""
        if order == 1:
            result = "first"
        elif order == 2:
            result = "second"
        else:
            result = "other"
        return result

    def get_random_sentence(self):
        return Text().sentence()

    def get_random_email(self):
        return Person().email()

    def get_random_job(self):
        return Person().occupation()

    def get_random_gender(self):
        """Generate a random gender."""
        gender = ["male", "female"]
        return random.choice(gender)

    def get_random_province(self):
        return Address().province()

    def get_unique_phone_number_set(self, min_length: int, digits: int) -> Set[str]:
        """Generates a unique set of phone number which is guaranteed to be
        bigger than a specified number and it contains given digits or
        characters given.

        PARAMS
        ------
        min_length: int:
            the minimum element_length of the resulting set
        digits: int:
            how many characters or digits should each phone number have.

        Returns
        -------
            a set containing unique phone numbers, its element_length is always
            somewhere between min_length and (min_length + 10)

        """
        phone_number_set = set(
            [self.get_random_telephone()[:digits] for _ in range(min_length)]
        )
        while len(phone_number_set) < min_length:
            phone_number_set = set.union(
                phone_number_set,
                set([self.get_random_telephone()[:digits] for _ in range(10)]),
            )
        return phone_number_set

    def get_currency_exchange(
        self, source_currency, source_value, rial_profit, toman_profit, usd_profit
    ):
        if source_currency == "R":
            target_value = int(int(source_value) * random.uniform(*rial_profit))
        elif source_currency == "T":
            target_value = int(int(source_value) * random.uniform(*toman_profit))
        else:
            target_value = round(int(source_value) * random.uniform(*usd_profit), 2)
        return target_value

    def get_voucher_kind(self, static_chance: int = 20):
        """Get a random kind of voucher.

        PARAMS:
        -----
        static_chance: int = 20:
            chance for every created voucher to be static.

        """

        kinds = ("static_based", "code_based")
        return random.choices(
            kinds, weights=(static_chance, (100 - static_chance)), k=1
        )[0]

    def get_voucher_type(self):
        """Get a random type for voucher."""
        types = ("fixed_price_based", "percentage_based")
        return random.choice(types)

    def get_voucher_status(self):
        """Get a random status for voucher."""
        status = ("open", "suspend", "consumed")
        return random.choice(status)

    def get_random_percentage(self, start: int = 1, end: int = 100):
        """Get a random percentage between given start and end numbers.

        raises a value error if given values are bellow0 or over 100 or
        if start is bigger than end.

        """
        if 100 < start < 0:
            raise ValueError(
                f"start has to be between 0 to 100" f",however given start is {start}"
            )
        elif 100 < end < 0:
            raise ValueError(
                f"end has to be between 0 to 100" f",however given start is {end}"
            )
        elif start > end:
            raise ValueError(
                f"start has to be smaller than end, however given"
                f"start is {start} and given end is {end}"
            )
        else:
            return random.randint(start, end)

    def get_unique_hashes_list(self, total: int, element_length: int = 12):
        """Get a set(which has unique elements) of hashes.

        PARAMS:
        total: int:
            length of the set.
        element_length: int = 12:
            length of each element in the set.

        """
        hash_set = {self.get_random_secret(element_length) for _ in range(total)}
        while len(hash_set) < total:
            hash_set = set.union(
                hash_set, {self.get_random_secret(element_length) for _ in range(10)}
            )
        return list(hash_set)[:total]

    def get_random_time_between_two_datetime_objects(
        self, time1: datetime, time2: datetime, tz: timezone = timezone.utc
    ):
        """Get a random datetime object between two given datetime objects.
        raises ValueError if start time is bigger than end time.

        PARAMS
        -----
        time1: datetime:
            start time.
        time2: datetime:
            end time.
        tz: timezone = timezone.utc:
            requested time zone, default is utc.

        """
        time1 = int(datetime.timestamp(time1))
        time2 = int(datetime.timestamp(time2))
        if time1 > time2:
            raise ValueError("start time is later than end time" f"{time1} > {time2}")
        random_time = random.randint(time1, time2)
        return datetime.fromtimestamp(random_time).replace(tzinfo=tz)

    def get_random_spice(self):
        """Gets the name of a random spice."""
        return Food().spices()

    def add_to_m2m(
        self, objs: List[Any], target_field: str, item_pre_obj: int, item: Type[T]
    ) -> None:
        """Add a number of randomly selected objects from a list to a
        ManyToManyField.

        This method selects `item_pre_obj` number of objects randomly from the `objs` list and adds them to the ManyToManyField
        on the model instance. The `objs` list must not be empty, or an `IndexError` will be raised.

        Args:
            self: An instance of the model.
            objs (List[Any]): A list of objects to select from.
            target_field (str): The name of the ManyToManyField on the model instance.
            item_pre_obj (int): The number of objects to add to the ManyToManyField.
            item (Type[T]): The type of the model that the ManyToManyField belongs to.

        Raises:
            IndexError: If the `objs` list is empty.

        Returns:
            None.

        """

        attr = getattr(item, target_field)
        try:
            items_to_add = list(map(lambda _: random.choice(objs), range(item_pre_obj)))
        except IndexError:
            raise IndexError("`objs` is empty. Please ensure population is not None.")
        attr.add(*items_to_add)
