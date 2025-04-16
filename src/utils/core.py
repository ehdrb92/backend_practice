def to_dict(obj) -> dict:
    """
    클래스 인스턴스의 모든 속성을 딕셔너리로 변환합니다.

    Args:
        obj: 변환할 클래스 인스턴스

    Returns:
        dict: 클래스의 속성들을 key-value 쌍으로 담은 딕셔너리
    """
    # vars() 함수를 사용하여 객체의 __dict__ 속성을 딕셔너리로 반환
    # 또는 getattr()를 사용하여 동적으로 속성에 접근할 수도 있습니다
    return vars(obj)


def to_dict_recursive(obj) -> dict:
    """
    클래스 인스턴스의 모든 속성을 재귀적으로 딕셔너리로 변환합니다.
    중첩된 객체들도 모두 딕셔너리로 변환됩니다.

    Args:
        obj: 변환할 클래스 인스턴스

    Returns:
        dict: 클래스의 속성들을 key-value 쌍으로 담은 딕셔너리
    """
    if not hasattr(obj, "__dict__"):
        return obj

    result = {}
    for key, value in vars(obj).items():
        if hasattr(value, "__dict__"):
            result[key] = to_dict_recursive(value)
        elif isinstance(value, list):
            result[key] = [to_dict_recursive(item) for item in value]
        elif isinstance(value, dict):
            result[key] = {k: to_dict_recursive(v) for k, v in value.items()}
        else:
            result[key] = value
    return result
