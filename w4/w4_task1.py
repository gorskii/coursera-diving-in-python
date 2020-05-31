"""
В этом задании вам нужно создать интерфейс для работы с файлами.
Класс File должен поддерживать несколько необычных операций.
"""

import os
import tempfile
import traceback


class File:
    """Interface to work with file objects."""

    # TODO: Переписать так, чтобы был и контекстный менеджер, и обычная
    #       инициализация
    # TODO: Инициализация полным путем
    def __init__(self, filename, mode='r+'):
        self._filename = filename
        self._mode = mode
        try:
            # FIXME: Не создавать инстанс, если файл не удалось открыть
            self._file = open(self.filename, self.mode)
        except FileNotFoundError:
            print(f"File '{self.filename}' not found")

    def __del__(self):
        print("__del__ '{}' object".format(self.filename))
        del self

    # def open(self):
    #
    def close(self):
        self.file.close()
        del self

    @property
    def filename(self):
        return self._filename

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value):
        # TODO: обрабатывать сочетания режимов
        if value in ('r', 'w', 'x', 'a', 'b', 't', '+', 'U', 'r+', 'w+'):
            self._mode = value
        else:
            raise ValueError(f'Invalid mode: {value}')

    @property
    def file(self):
        return self._file

    def read(self):
        # TODO: Проверка на существование file
        return str(self.file.readline())

    def write(self, string):
        # FIXME: вызывается, даже если не был открыт файл при инициализации

        # Файл открылся
        if self.file is not None and self.mode != 'r':
            try:
                self.file.write(string)
            except IOError as err:
                # FIXME: Обработать исключение правильно
                print(err)

    def __str__(self):
        return self.filename

    def __iter__(self):
        return self

    def __next__(self):
        current = self.file.readline()
        if current == '':
            raise StopIteration
        return current

    def __add__(self, other):
        tmp_path = os.path.join(tempfile.gettempdir(), "tmpfile.txt")
        tmp_file = File(tmp_path, 'w+')
        for line in self:
            tmp_file.write(line)
        for line in other:
            tmp_file.write(line)
        return tmp_file

    def __enter__(self):
        print("__enter__ '{}' context".format(self.filename))
        # self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__ '{}' context".format(self.filename))
        self.close()


# Класс инициализируется полным путем.
obj = File('tmp/file.txt')

# Класс должен поддерживать метод write.
if obj is not None:
    obj.write('line\n')

# Объекты типа File должны поддерживать сложение.
first = File('tmp/first')
second = File('tmp/second')

new_obj = first + second
# В этом случае создается новый файл и файловый объект, в котором содержимое
# второго файла добавляется к содержимому первого файла. Новый файл должен
# создаваться в директории, полученной с помощью tempfile.gettempdir.
# Для получения нового пути можно использовать os.path.join.


# Должна быть итерация по строкам
print('About to iterate')
new_obj.file.seek(0)
for line in new_obj:
    print(line)

# При выводе файла должен печататься его полный путь,
# переданный при инициализации
print(obj)
# >> '/tmp/file.txt'

with File('tmp/first') as f:
    for line in f:
        print(line, end='')
