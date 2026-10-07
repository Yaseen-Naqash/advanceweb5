import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model

from base.models import Property, Attribute, City

User = get_user_model()

# ---------- Farsi dummy data pools ----------

CITIES = [
    'تهران', 'مشهد', 'اصفهان', 'شیراز', 'تبریز',
    'کرج', 'اهواز', 'قم', 'کرمانشاه', 'رشت',
    'یزد', 'ارومیه', 'زاهدان', 'کرمان', 'همدان',
]

ATTRIBUTES = [
    'استخر', 'آسانسور', 'بالکن', 'انبار', 'پارکینگ',
    'حیاط', 'روف گاردن', 'سرمایش و گرمایش', 'درب ضد سرقت',
    'کولر گازی', 'پکیج', 'آنتن مرکزی', 'سیستم اعلام حریق',
    'نگهبانی', 'دوربین مداربسته',
]

TITLES_BY_TYPE = {
    '0': [  # آپارتمان
        'آپارتمان {area} متری {rooms} خوابه',
        'آپارتمان لوکس {area} متری',
        'آپارتمان نوساز {rooms} خوابه در {city}',
        'آپارتمان فول امکانات {area} متری',
    ],
    '1': [  # ویلا
        'ویلا {area} متری با حیاط',
        'ویلا دوبلکس {rooms} خوابه',
        'ویلا باغ {area} متری',
        'ویلا ساحلی {rooms} خوابه',
    ],
    '2': [  # تجاری
        'مغازه تجاری {area} متری',
        'واحد تجاری پاساژ {area} متری',
        'ملک تجاری بر خیابان اصلی',
    ],
    '3': [  # اداری
        'دفتر کار اداری {area} متری',
        'واحد اداری {rooms} اتاقه',
        'مطب اداری در برج {city}',
    ],
    '4': [  # زمین
        'زمین {area} متری با سند',
        'زمین مسکونی {area} متری',
        'زمین تجاری {area} متری',
    ],
}

FIRST_NAMES = [
    'علی', 'محمد', 'رضا', 'حسین', 'امیر', 'مهدی', 'سعید', 'فرهاد',
    'زهرا', 'فاطمه', 'مریم', 'سارا', 'نرگس', 'الهام', 'شیما', 'پریسا',
]

LAST_NAMES = [
    'محمدی', 'حسینی', 'رضایی', 'احمدی', 'کریمی', 'موسوی',
    'جعفری', 'قاسمی', 'صادقی', 'نوری', 'عباسی', 'رحیمی',
]

BACKYARD_OPTIONS = ['ندارد', 'حیاط کوچک', 'حیاط بزرگ', 'روف گاردن', 'تراس']
ROOMS_OPTIONS = ['۱', '۲', '۳', '۴', '۵', 'بدون اتاق']


class Command(BaseCommand):
    help = 'Generate dummy Farsi data for Property, Attribute, City and Person models'

    def add_arguments(self, parser):
        parser.add_argument(
            '--properties',
            type=int,
            default=50,
            help='Number of Property records to create (default: 50)',
        )
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of User records to create (default: 10)',
        )
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete existing dummy data before generating new ones',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        n_props = options['properties']
        n_users = options['users']
        flush = options['flush']

        if flush:
            self.stdout.write(self.style.WARNING('Deleting existing data...'))
            Property.objects.all().delete()
            Attribute.objects.all().delete()
            City.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()

        # ---------- Cities ----------
        self.stdout.write('Creating cities...')
        cities = []
        for title in CITIES:
            city, _ = City.objects.get_or_create(title=title)
            cities.append(city)

        # ---------- Attributes ----------
        self.stdout.write('Creating attributes...')
        attributes = []
        for title in ATTRIBUTES:
            attr, _ = Attribute.objects.get_or_create(
                title=title,
                defaults={'is_included': random.choice([True, False])},
            )
            attributes.append(attr)

        # ---------- Users ----------
        self.stdout.write('Creating users...')
        users = []
        for i in range(n_users):
            first = random.choice(FIRST_NAMES)
            last = random.choice(LAST_NAMES)
            username = f'user_{i}_{random.randint(1000, 9999)}'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'first_name': first,
                    'last_name': last,
                    'email': f'{username}@example.com',
                    'phone': f'09{random.randint(100000000, 999999999)}',
                    'gender': random.choice(['0', '1']),
                    'external_id': f'ext_{random.randint(10000, 99999)}',
                },
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        # ---------- Properties ----------
        self.stdout.write(f'Creating {n_props} properties...')
        type_keys = [t[0] for t in Property.TYPE]
        deal_keys = [d[0] for d in Property.DEAL_TYPE]

        created_count = 0
        for _ in range(n_props):
            city = random.choice(cities)
            p_type = random.choice(type_keys)
            area = random.randint(40, 500)
            rooms = random.choice(ROOMS_OPTIONS)

            title_template = random.choice(TITLES_BY_TYPE[p_type])
            title = title_template.format(
                area=area,
                rooms=rooms,
                city=city.title,
            )

            # price depends on deal type
            deal_type = random.choice(deal_keys)
            if deal_type == '0':  # خرید
                price = random.randint(500_000_000, 50_000_000_000)
            else:  # اجاره
                price = random.randint(5_000_000, 200_000_000)

            prop = Property.objects.create(
                title=title,
                rooms=rooms,
                parking=random.choice([True, False]),
                backyard=random.choice(BACKYARD_OPTIONS),
                price=price,
                type=p_type,
                deal_type=deal_type,
                area=area,
                city=city,
            )

            # attach 2-6 random attributes
            sample_attrs = random.sample(
                attributes, k=random.randint(2, min(6, len(attributes)))
            )
            prop.Attributes.set(sample_attrs)

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Successfully created:\n'
                f'   - {len(cities)} cities\n'
                f'   - {len(attributes)} attributes\n'
                f'   - {len(users)} users\n'
                f'   - {created_count} properties'
            )
        )