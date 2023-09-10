from split_settings.tools import include

base_settings: tuple[str, ...] = (
    'components/common.py',
    'components/database.py',
    'components/apps.py',
    'components/middleware.py',
    'components/validation.py',
    'components/rendering.py',
    'components/timezone.py',
    'components/locale.py',
)

include(*base_settings)
