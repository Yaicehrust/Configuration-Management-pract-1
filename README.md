# VFS Shell Emulator

Этап 1 практической работы по дисциплине «Конфигурационное управление».

## Описание

Программа представляет собой графический эмулятор командной оболочки.
На этапе 1 реализованы REPL, разбор команд с поддержкой кавычек,
заглушки команд `ls` и `cd`, а также команда `exit`.

## Запуск

Windows:

```text
run.bat
```

Или:

```text
python -m src.main
```

## Тесты

```text
python -m unittest discover -s tests -v
```

## Примеры

```text
ls
cd Documents
ls "My Documents"
unknown
exit
```
