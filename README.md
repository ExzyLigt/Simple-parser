# Парсер похожих товаров

Парсер разработан для интернет-магазина освещения, чтобы парсить артикулы похожих товаров с сайта поставщика. 
Входными данными является файл, содержащий список артикулов в json формате( *пример json файла находится в* **/documents/data.json**), выходными данными является файл либо в **xlsx** формате, либо в **json** формате.

## Установка
1. Необходимо клонировать проект на локальную машину:

```bash
git clone 
```

2. В проекте используется *pyproject.toml*, чтобы установить зависимости из этого файла необходимо воспользоваться пакетным менеджером [***poetry***](https://pypi.org/project/poetry/). Если *poetry* не установлен необходимо выполнить команду:

### Для OSX/Linux/bashonwindows

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

### Для Windows Powershell
```bash
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

3. Создаем виртуальное окружение:

```bash
poetry shell
```   

4. Устанавливаем зависимости в созданное виртуальное окружение:

```bash
poetry install
```   

## Использование 

Парсер находится в директории *parser2/sync_parser.py*. Для того чтобы запустить парсер необходимо выполнить команду:

```bash
python path/to/sync_parser.py /relative/path/to/json_file [-t, --type] [xlsx, json]  
```   

Где **path/to/sync_parser.py** является путем до скрипта *sync_parser.py* относительно текущей директории, */relative/path/to/json_file* является путем до json файла относительно текущей директории(**является обязательным параметром**), *-t или --type* является типом выходного файла с выбором между xlsx и json(**необязательный параметр, по умолчанию стоит xlsx**).

Пример полученного json файла находится в **/documents/n.json** .


## P.S.
Скорость выполнения полного скрипта ***~30 МИН.***, из-за того что нет тредов или асинхронности(будет в скором времени). Поэтому чтобы не ждать столько, можно взять срез в функции *main()*, строка 169, допустим из 10-20 артикулов. 

```python
articuls = create_list_from_json(json_file)[:20]
```