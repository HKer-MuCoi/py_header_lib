# -*- coding: utf-8 -*-
def paginate_format(pagination):
    pagination.__dict__['pages'] = int(pagination.total / pagination.per_page) + (
        1 if pagination.total % pagination.per_page > 0 else 0)
    pagination.__dict__['has_previous'] = True if pagination.page > 1 else False
    pagination.__dict__['has_next'] = True if pagination.page < pagination.pages else False
    pagination.__dict__['next_page'] = pagination.page + 1 if pagination.has_next is True else None
    pagination.__dict__['previous_page'] = pagination.page - 1 if pagination.has_previous is True else None
    return pagination


def convert_models_to_dict(models):
    return [model.json for model in models]


def group_by_name(name, items):
    group = dict()
    for item in items:
        group_is_exist = group.get(item.get(name))
        if group_is_exist is None:
            group_is_exist = []
        group_is_exist.append(item)
        group.update({
            item.get(name): group_is_exist
        })
    return group


def beautiful_to_dict(data: dict) -> dict:
    return {key: value for key, value in data.items() if value is not None}


def remove_none_in_dict(data: dict) -> dict:
    return {key: value for key, value in data.items() if value is not None}
