# from dataclasses import dataclass, field
# from typing import Set
#
# from project.domain.value_objects.file_name_keeper import FileName
#
#
# @dataclass
# class FileNameKeeper:
#     """
#     Хранит имена файлов из директории кеша без повторного чтения.
#     Сохраняет только уникальные имена.
#     """
#     _filenames: Set[str] = field(default_factory=set)
#
#     def add(self, filename: FileName) -> None:
#         """Добавляет имя файла в состояние."""
#         self._filenames.add(filename.name)
#
#     def exists(self, filename: FileName) -> bool:
#         """
#         Проверяет, есть ли имя файла в состоянии.
#         Принимает Path (из ФС) или FileName (модель).
#         """
#         if isinstance(filename, FileName):
#             return filename.name in self._filenames
#         return filename.name in self._filenames
#
#     @property
#     def filenames(self) -> Set[str]:
#         """Возвращает текущее состояние."""
#         return self._filenames.copy()
