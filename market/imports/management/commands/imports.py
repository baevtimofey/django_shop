from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from imports.services import Imports


class Command(BaseCommand):
    """Кастомная команда Джанго, для запуска импорта продуктов загруженных пользователем."""

    def add_arguments(self, parser):
        """Добавление аргументов в команду."""
        parser.add_argument('file', type=str, nargs='+', help=_('Имя файла'))

    def handle(self, *args, **kwargs):
        """Логика выполнения команды."""
        imports = Imports()
        if ''.join(kwargs['file']) == 'all':
            self.stdout.write(_('Импорт запущен...'))
            imports.imports_all_files()
            self.stdout.write(_('Импорт завершён.'))
        elif len(kwargs['file']) == 1:
            self.stdout.write(_('Импорт одного файла запущен...'))
            imports.import_file(file_name=kwargs['file'])
            self.stdout.write(_('Импорт одного файла завершён.'))
        else:
            self.stdout.write(_('Импорт нескольких файлов запущен...'))
            imports.import_files(files=kwargs['file'])
            self.stdout.write(_('Импорт нескольких файлов завершён.'))
