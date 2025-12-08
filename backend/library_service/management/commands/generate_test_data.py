# library_service/management/commands/generate_test_data.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
import random
from faker import Faker
from library_service.models import (
    UserProfile, 
    Basket, 
    BasketItem, 
    Order, 
    OrderHistory, 
    OrderItem, 
    Library,
    LibraryDatabase
)

User = get_user_model()

class Command(BaseCommand):
    help = 'Generate test data for library service'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Clear existing data first')

    def handle(self, *args, **options):
        fake = Faker('ru_RU')
        
        self.stdout.write('Starting data generation...')
        
        if options['flush']:
            self.stdout.write('Clearing existing data...')
            self.clear_data()
        
        # Создаем библиотеки если их нет
        libraries = self.create_libraries()
        
        # Создаем пользователей и профили (100 пользователей)
        users = self.create_users_and_profiles(100, fake)
        
        if not users:
            self.stdout.write(self.style.ERROR('❌ No users created. Stopping.'))
            return
        
        # Создаем корзины (1 к 1 с пользователями)
        baskets = self.create_baskets(users, fake)
        
        # Создаем заказы (200 заказов)
        orders = self.create_orders(200, users, libraries, fake)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'''✅ Successfully created:
                - {len(users)} users with profiles
                - {len(baskets)} baskets with items (1:1 with users)
                - {len(orders)} orders with history and items'''
            )
        )

    def clear_data(self):
        """Очистка существующих данных"""
        OrderItem.objects.all().delete()
        OrderHistory.objects.all().delete()
        Order.objects.all().delete()
        BasketItem.objects.all().delete()
        Basket.objects.all().delete()
        UserProfile.objects.all().delete()
        # Не удаляем пользователей и библиотеки

    def create_libraries(self):
        """Создание тестовых библиотек если их нет"""
        libraries = Library.objects.all()
        if not libraries.exists():
            self.stdout.write('Creating libraries...')
            lib1 = Library.objects.create(
                description="ИРНИТУ",
                address="664074, Россия, г. Иркутск, ул. Лермонтова, 83."
            )
            LibraryDatabase.objects.create(database="ISTU", library=lib1)
            libraries = Library.objects.all()
            self.stdout.write('📚 Created libraries')
        else:
            self.stdout.write(f'📚 Using existing {libraries.count()} libraries')
        return list(libraries)

    def create_users_and_profiles(self, count, fake):
        """Создание пользователей и профилей"""
        users = []
        departments = [
            "Институт компьютерных наук",
            "Факультет экономики", 
            "Исторический факультет",
            "Медицинский институт",
            "Филологический факультет",
            "Инженерный отдел",
            "Физический факультет",
            "Химический факультет",
            "Биологический факультет",
            "Юридический факультет"
        ]
        
        created_count = 0
        for i in range(count):
            try:
                first_name = fake.first_name()
                last_name = fake.last_name()
                username = f"test_user_{i}_{fake.user_name()}"
                
                # Пропускаем если пользователь уже существует
                if User.objects.filter(username=username).exists():
                    continue
                
                user = User.objects.create_user(
                    username=username,
                    email=fake.email(),
                    password='testpass123',
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Создаем профиль
                profile = UserProfile.objects.create(
                    user=user,
                    library_card=f"LC{fake.unique.random_number(digits=8)}",
                    campus_id=f"CAMPUS{fake.random_number(digits=6)}" if fake.boolean(70) else None,
                    mira_id=f"MIRA{fake.random_number(digits=5)}" if fake.boolean(60) else None,
                    fullname=f"{last_name} {first_name} {fake.middle_name()}",
                    department=random.choice(departments)
                )
                users.append(user)
                created_count += 1
                
            except Exception as e:
                self.stdout.write(self.style.WARNING(f"⚠️ Error creating user {i}: {e}"))
        
        # Если не создали новых пользователей, используем существующих (кроме суперпользователей)
        if not users:
            users = list(User.objects.filter(is_superuser=False)[:count])
            self.stdout.write(f'👥 Using existing {len(users)} users')
        else:
            self.stdout.write(f'👥 Created {created_count} new users with profiles')
        
        return users

    def create_baskets(self, users, fake):
        """Создание корзин (1 к 1 с пользователями)"""
        baskets = []
        # Генерируем много книг для разнообразия
        book_ids = [f"BOOK{fake.unique.random_number(digits=6)}" for _ in range(500)]
        
        for user in users:
            # Проверяем, есть ли уже корзина у пользователя
            if Basket.objects.filter(user=user).exists():
                basket = Basket.objects.get(user=user)
            else:
                # Создаем корзину для каждого пользователя
                basket = Basket.objects.create(user=user)
            
            baskets.append(basket)
            
            # Очищаем старые элементы корзины
            BasketItem.objects.filter(basket=basket).delete()
            
            # Добавляем элементы в корзину (0-7 книг, может быть пустая)
            num_items = random.randint(0, 7)
            if num_items > 0:
                selected_books = random.sample(book_ids, min(num_items, len(book_ids)))
                
                for book_id in selected_books:
                    BasketItem.objects.create(
                        book_id=book_id,
                        basket=basket
                    )
        
        self.stdout.write(f'🛒 Created/updated {len(baskets)} baskets (1:1 with users)')
        return baskets

    def create_orders(self, count, users, libraries, fake):
        """Создание заказов с историей и элементами"""
        orders = []
        
        for i in range(count):
            user = random.choice(users)
            library = random.choice(libraries)
            
            order = Order.objects.create(
                user=user,
                library=library
            )
            orders.append(order)
            
            # Создаем историю заказа с конечными статусами только в конце
            self.create_order_history(order, users, fake)
            
            # Создаем элементы заказа (1-7 книг)
            self.create_order_items(order, fake)
            
            if i % 50 == 0 and i > 0:
                self.stdout.write(f'📦 Created {i} orders...')
        
        self.stdout.write(f'📦 Created {len(orders)} orders total')
        return orders

    def create_order_history(self, order, users, fake):
        """Создание истории статусов для заказа с конечными статусами только в конце"""
        current_time = timezone.now()
        order_start_date = current_time - timedelta(days=random.randint(1, 60))
        
        non_final_statuses = ["new", "processing", "ready", "error"]
        final_statuses = ["done", "cancelled", "archived"]
        
        # Определяем, будет ли заказ завершенным
        is_final = random.random() < 0.7  # 70% заказов завершены
        
        if is_final:
            # Для завершенных заказов: нефинальные статусы -> финальный статус
            num_events = random.randint(2, 5)
            status_sequence = []
            
            # Добавляем нефинальные статусы
            for _ in range(num_events - 1):
                status_sequence.append(random.choice(non_final_statuses))
            
            # Добавляем финальный статус в конце
            status_sequence.append(random.choice(final_statuses))
        else:
            # Для незавершенных заказов: только нефинальные статусы
            num_events = random.randint(1, 4)
            status_sequence = [random.choice(non_final_statuses) for _ in range(num_events)]
        
        # Убираем дубликаты подряд и гарантируем, что начинается с "new"
        if status_sequence[0] != "new":
            status_sequence.insert(0, "new")
        
        # Создаем уникальную последовательность без повторений подряд
        unique_sequence = []
        for status in status_sequence:
            if not unique_sequence or status != unique_sequence[-1]:
                unique_sequence.append(status)
        
        # Создаем события истории
        for i, status in enumerate(unique_sequence):
            days_offset = i * random.randint(1, 3)  # Каждое событие через 1-3 дня
            event_date = order_start_date + timedelta(days=days_offset)
            
            staff = random.choice(users) if status != "new" else None
            
            OrderHistory.objects.create(
                description=self.get_status_description(status, fake),
                status=status,
                date=event_date,
                order=order,
                staff=staff
            )

    def get_status_description(self, status, fake):
        """Генерация описания для статуса"""
        descriptions = {
            "new": "Заказ создан",
            "processing": "Заказ в обработке",
            "ready": "Заказ готов к выдаче", 
            "error": "Возникла ошибка при обработке",
            "done": "Заказ выполнен успешно",
            "cancelled": "Заказ отменен",
            "archived": "Заказ перемещен в архив",
        }
        
        base_description = descriptions.get(status, "Изменение статуса")
        
        # Добавляем случайные детали для нефинальных статусов
        if status in ["new", "processing", "ready", "error"]:
            details = [
                "Ожидание подтверждения",
                "Проверка наличия книг",
                "Согласование с отделом",
                "Уточнение деталей",
                "Обработка данных",
                "Подготовка документов",
                "Ожидание выдачи",
                "Проверка читательского билета"
            ]
            
            if random.random() < 0.6:
                return f"{base_description}. {random.choice(details)}."
        
        return base_description

    def create_order_items(self, order, fake):
        """Создание элементов заказа (1-7 книг)"""
        num_items = random.randint(1, 7)
        book_ids = [f"ORDER_BOOK{fake.random_number(digits=6)}" for _ in range(num_items)]
        
        # Определяем общий статус заказа из его истории
        final_status = order.statuses.last().status
        
        order_items = []
        
        for book_id in book_ids:
            if final_status == "done":
                item_status = random.choice(["handed", "returned"])
            elif final_status == "cancelled":
                item_status = random.choice(["ordered", "cancelled"])
            elif final_status == "archived":
                item_status = random.choice(["handed", "returned", "ordered"])
            else:
                item_status = "ordered"
            
            handed_date = None
            to_return_date = None
            returned_date = None
            
            if item_status in ["handed", "returned"]:
                handed_date = timezone.now().date() - timedelta(days=random.randint(5, 30))
                to_return_date = handed_date + timedelta(days=14)
                
                if item_status == "returned":
                    returned_date = handed_date + timedelta(days=random.randint(1, 13))
            
            order_item = OrderItem.objects.create(
                order=order,
                book_id=book_id,
                status=item_status,
                description=fake.sentence() if fake.boolean(40) else None,
                handed_date=handed_date,
                to_return_date=to_return_date,
                returned_date=returned_date
            )
            order_items.append(order_item)
        
        # Создаем некоторые связи analogous_order_item (редко)
        if len(order_items) > 1 and random.random() < 0.1:
            item1, item2 = random.sample(order_items, 2)
            item1.analogous_order_item = item2
            item1.save()