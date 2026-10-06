# VFS Shell Emulator

Практическая работа по «Конфигурационному управлению», вариант №1.

## Этап 4

Реализованы `ls`, `cd`, `du` и `cal`. Все операции с VFS выполняются
над деревом в памяти.

Поддерживаемые варианты команд:

```text
ls
ls PATH
ls -l [PATH]
cd [PATH]
du [-s] [-h] [PATH]
cal
cal YEAR
cal MONTH YEAR
```

## Запуск

```text
python -m src.main --vfs data/vfs/nested.csv --script scripts/stage4_start.txt
```

## Тесты

```text
python -m unittest discover -s tests -v
```
