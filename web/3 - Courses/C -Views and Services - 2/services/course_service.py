from decimal import Decimal as dec
from typing import List
from data.models import Course


def course_count() -> int:
    return 199


def most_popular_courses(count: int) -> List[Course]:
    return [
        Course(
            id=1,
            category='Hotelaria e Turismo',
            price=dec(179),
            name='Gestor Turístico',
            summary='Et architecto provident deleniti facere repellat nobis iste. Id facere quia quae dolores dolorem tempore.',
            trainer_id=1,
            trainer_name='Osmar',

        ),
        Course(
            id=2,
            category='Programação em C++',
            price=dec(250),
            name='Estruturas de Dados em C++',
            summary='Et architecto provident deleniti facere repellat nobis iste. Id facere quia quae dolores dolorem tempore.',
            trainer_id=4,
            trainer_name='Bernardo',
        ),
        Course(
            id=3,
            category='Natação',
            price=dec(250),
            name='Estilo Borboleta',
            summary='Et architecto provident deleniti facere repellat nobis iste. Id facere quia quae dolores dolorem tempore.',
            trainer_id=2,
            trainer_name='Alberta',
        ),
    ][:count]


def available_courses(count: int) -> List[Course]:
    return [
        Course(
            id=5,
            category='Programação Web',
            price=dec(190),
            name='Desenvolvimento de Websites',
            summary='Consectetur et, temporibus velit inventore porro sint dolore hic veniam sapiente, quos voluptatem aliquid, explicabo doloremque sunt!',
            trainer_id=1,
            trainer_name='Osmar',
        ),
        Course(
            id=6,
            category='Marketing',
            price=dec(250),
            name='SEO - Optimizações Motores de Busca',
            summary='Et architecto provident deleniti facere repellat nobis iste. Id facere quia quae dolores dolorem tempore.',
            trainer_id=4,
            trainer_name='Bernardo',
        ),
        Course(
            id=7,
            category='Programação',
            price=dec(250),
            name='Programação de Device Drivers',
            summary='Ex voluptatibus amet magnam maxime. Repellat quis eos laudantium magnam alias quisquam repellendus magni, quas nam vitae explicabo sed necessitatibus? Eaque!',
            trainer_id=2,
            trainer_name='Alberta',

        ),
        Course(
            id=8,
            category='Electrónica',
            price=dec(280),
            name='Microsoldadura de SMD',
            summary=' Esse est nemo dolorum tempora numquam dolorem in optio sed quasi voluptate! Voluptatibus animi accusantium ad! Ratione et possimus repellendus vero nemo id modi.',
            trainer_id=6,
            trainer_name='Roberta',
        ),
    ][:count]
