# VFS Shell Emulator

Эмулятор UNIX-подобной оболочки, практическая работа, вариант №1.

## Этап 1

GUI, заглушки `ls` и `cd`, парсер с кавычками и `exit`.

## Этап 2

Поддерживаются параметры запуска `--vfs` и `--script`, отладочный вывод
параметров и выполнение стартового скрипта с комментариями.

## Запуск

```text
run.bat
```

С параметрами:

```text
python -m src.main --vfs stage2-vfs.csv --script scripts/stage2_start.txt
```

## Тесты

```text
python -m unittest discover -s tests -v
```
