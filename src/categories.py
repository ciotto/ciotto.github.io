# Categories
from models import Category

electronics = Category(
    slug='electronics',
    name='Electronics',
    icon='fas fa-microchip',
    page=None,
)
teardowns = Category(
    parent=electronics,
    slug='teardowns',
    name='Teardowns',
    icon='fas fa-tools',
    page=None,
)
boards = Category(
    parent=electronics,
    slug='boards',
    name='Boards',
    page=None,
)
arduino = Category(
    parent=boards,
    slug='arduino',
    name='Arduino',
    page=None,
)
coding = Category(
    slug='coding',
    name='Coding',
    icon='fas fa-keyboard',
    page=None,
)
python = Category(
    parent=coding,
    slug='python',
    name='Python',
    icon='fab fa-python',
    page=None,
)
system = Category(
    slug='system',
    name='System',
    icon='fas fa-server',
    page=None,
)
category_list = [
    electronics,
    teardowns,
    boards,
    arduino,
    coding,
    python,
    system,
]
main_categories = [c for c in category_list if not c.parent]
