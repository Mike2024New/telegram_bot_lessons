import json


def read_json(file_path: str) -> dict:
    """
    Чтение файла json
    :param file_path: путь к файлу
    :return: словарь из json
    """
    try:
        with open(file=file_path, mode="r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def rec_json(file_path: str, data: dict):
    """

    :param file_path:
    :param data:
    :return:
    """
    with open(file=file_path, mode="w", encoding="utf-8") as f:
        json.dump(data, f)


if __name__ == '__main__':
    rec_json(file_path="test.json", data={"new": 456, "proba": 123})
    # res = read_json(file_path="test.json")
    # print(res)
