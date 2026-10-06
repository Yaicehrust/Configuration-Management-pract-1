# VFS Shell Emulator

Практическая работа по «Конфигурационному управлению», вариант №1.

## Этапы 1–3

Проект содержит GUI, REPL, парсер с кавычками, параметры `--vfs` и
`--script`, стартовые скрипты и загрузку VFS из CSV в память.

VFS хранится в виде дерева. Вложенность задаётся абсолютными путями,
например `/home/user/file.txt`. Данные файлов представлены в Base64.
Исходный CSV не изменяется при работе программы.

## Запуск

```text
python -m src.main --vfs data/vfs/nested.csv --script scripts/stage3_nested.txt
```

## Тесты

```text
python -m unittest discover -s tests -v
```
