import os
import json


PATH = os.getenv('APPDATA') + '/.minecraft/assets'


def read_json(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def get_text(hash: str) -> str:
    lang = read_json(f'{PATH}/objects/{hash[:2]}/{hash}')
    return lang['subtitles.entity.fishing_bobber.splash'].strip()


def extract_lang_text() -> dict:
    data = dict()
    indexes = read_json(f'{PATH}/indexes/5.json')
    for k, v in indexes['objects'].items():
        if 'minecraft/lang' in k and '.json' in k:
            name = k.split('/')[-1].replace('.json', '')
            data[name] = get_text(v['hash'])
    return data


if __name__ == '__main__':
    data = extract_lang_text()
    print(data)

    with open('lang.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
