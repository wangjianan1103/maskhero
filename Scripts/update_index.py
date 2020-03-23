#!/usr/bin/python

import os
import json
import logging as log

root_path = os.path.abspath(os.path.dirname(os.getcwd()))


def collect_requirements(_country):
    log.info("Collecting %s" % _country)
    data_list = []
    dir_path = root_path + "/" + _country
    for filename in os.listdir(dir_path):
        if filename.endswith(".geo.json"):
            with open(dir_path + "/" + filename, 'r') as json_file:
                country_modal = json.load(json_file)
                if country_modal['features']:
                    for feature in country_modal['features']:
                        data_list.append(feature['properties'])

    return data_list


def update_country_index(_country, requirements):
    country_path = root_path + "/" + _country + "/index.geojson"
    write_file(country_path, requirements)

    _country_summary = {}
    if requirements and len(requirements) > 0:
        for requirement in requirements:

            for key, value in requirement.items():
                if key in '国家':
                    set_country_summary_dict(_country_summary, 'name', value, 1)
                elif key in ('需要援助人数', '需求数量', '收到数量'):
                    dict_name = ''
                    if key == '需要援助人数':
                        dict_name = 'beneficiaries'
                    elif key == '需求数量':
                        dict_name = 'masks_requested'
                    elif key == '收到数量':
                        dict_name = 'masks_delivered'
                    set_country_summary_dict(_country_summary, dict_name, value, 0)
                elif key in '申请人':
                    set_country_summary_dict(_country_summary, 'applicants', 1, 0)

    return _country_summary


def write_file(path_, data_list):
    if not os.path.exists(path_):
        f = open(path_, "a")
        f.write("{}")
        f.close()

    with open(path_, 'r') as f:
        update_data = json.load(f)
        features_list = []
        for requirement in data_list:
            features_list.append(requirement)
        update_data['features'] = features_list

    with open(path_, 'w') as file_:
        json.dump(update_data, file_, ensure_ascii=False, indent=4)


def set_country_summary_dict(_dict, key, default, operate):
    if operate == 1:
        _dict.setdefault(key, default)
        return

    if _dict.__contains__(key):
        _dict[key] = (_dict.get(key) + default)
    else:
        _dict.setdefault(key, default)


def append_world_index(_requirements):
    world_path = root_path + "/World/index.geojson"
    write_file(world_path, _requirements)
    pass


if __name__ == '__main__':
    log.basicConfig(level=log.INFO)

    countries = ["Canada"]

    world_summary = {
        "name": "World",
        "applicants": 0,
        "beneficiaries": 0,
        "masks_requested": 0,
        "masks_delivered": 0
    }
    world_summary_requirements = []

    for country in countries:
        country_requirements = collect_requirements(country)
        country_summary = update_country_index(country, country_requirements)
        world_summary_requirements.append(country_summary)
    append_world_index(world_summary_requirements)
