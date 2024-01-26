from modules.adapters.replacers.replacer import crawler


def test_replacer_should_replace_values_in_dict():
    # Arrange
    d = {"a": "${asd}"}
    body = {"asd": 1}

    # Act
    crawler(d, body)

    # Assert
    d["a"] == body["asd"]


def test_replacer_should_replace_values_in_list():
    # Arrange
    d = ["${asd}", "${asd}"]
    body = {"asd": 1}

    # Act
    crawler(d, body)

    # Assert
    d[0] == str(body["asd"])
    d[1] == str(body["asd"])

def test_replacer_should_replace_values_in_list_of_dicts():
    # Arrange
    d = [{"first": "${asd}"}, {"second": "${asd}"}]
    body = {"asd": 1}

    # Act
    crawler(d, body)

    # Assert
    d[0]["first"] == body["asd"]
    d[1]["second"] == body["asd"]

def test_replacer_should_replace_values_in_lists_of_dicts_strings_with_levels_of_refference():
    # Arrange
    d = [{"first": "${main.target}"}, {"second": "${main.target}"}]
    body = {"main": {"target": 1}}

    # Act
    crawler(d, body)

    # Assert
    d[0]["first"] == body["main"]["target"]
    d[1]["second"] == body["main"]["target"]

def test_replacer_should_replace_values_in_lists_of_dicts_strings_with_levels_of_refference_and_multiple_different_placeholders(): # noqa
    # Arrange
    d = [{"first": "${main.target1} : ${main.target2}"}, {"second": "${main.target1} : ${main.target2}"}]
    body = {"main": {"target1": 1, "target2": 2}}

    # Act
    crawler(d, body)

    # Assert
    target1=body["main"]["target1"]
    target2=body["main"]["target2"]
    d[0]["first"] == f"{target1} : {target2}"
    d[1]["second"] == f"{target1} : {target2}"