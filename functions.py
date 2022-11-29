import requests
from lxml import etree
import data

VANILLA_VERSION_MANIFEST = {
    'MOJANG': 'https://piston-meta.mojang.com/mc/game/version_manifest_v2.json',
    'BMCL': 'https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json',
}

FORGE_API = {
    'BMCL_MCVERSION': 'https://bmclapi2.bangbang93.com/forge/minecraft'
}

FABRIC_API = {
    'FABRIC_MCVERSION': 'https://meta.fabricmc.net/v2/versions',
}

SPIGOT_API = {
    'SPIGOT_VERSIONS_API': "https://hub.spigotmc.org/versions/",
}

PAPER_API = {
    'VERSIONS': 'https://api.papermc.io/v2/projects/paper/',
}


def get_serverside_version_list(serverside, mirror='BMCL'):
    res = []
    match serverside:
        case 'Vanilla':
            r = requests.get(VANILLA_VERSION_MANIFEST[mirror]).json()
            for _ in r['versions']:
                res.append(_['id'])
        case 'Forge':
            res = requests.get(FORGE_API['BMCL_MCVERSION']).json()
            res.sort(key=lambda x: tuple(int(v) if v.isdigit()
                                         else int(''.join(filter(lambda _: _.isdigit(), list(v))))
                                         for v in x.split('.')), reverse=True)
        case 'Fabric':
            r = requests.get(FABRIC_API['FABRIC_MCVERSION']).json()
            # res = [_['version'] for _ in res['game']]
            res = [f"{_['gameVersion']}{_['separator']}{_['build']}"
                   for _ in r['mappings']]
        case 'Spigot':
            r = requests.get(SPIGOT_API['SPIGOT_VERSIONS_API']).text
            res = list({_[:-5] if '1.1' in _ else None
                        for _ in etree.HTML(r).xpath('//@href')})[:-1]
            res.sort(key=lambda x: tuple(int(y) if y.isdigit()
                                         else int(y[:-5])
                                         for y in x.split('.')), reverse=True)
        case 'Paper':
            res = requests.get(PAPER_API['VERSIONS']).json()['versions'][::-1]
    return res


def get_link(serverside, version, mirror='BMCL'):
    res = ''
    match serverside:
        case 'Vanilla':
            for _ in requests.get(VANILLA_VERSION_MANIFEST[mirror]).json()['versions']:
                if _['id'] == version:
                    return requests.get(_['url']).json()['downloads']['server']['url']
        case 'Forge':
            pass


def install_server(sc: data.ServerConfig):
    pass


# TEST:
if __name__ == '__main__':
    print(get_serverside_version_list('Spigot'))
