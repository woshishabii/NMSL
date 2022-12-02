import os

import requests
from lxml import etree
import shutil
import wx
import subprocess

import data

VANILLA_VERSION_MANIFEST = {
    'MOJANG': 'https://piston-meta.mojang.com/mc/game/version_manifest_v2.json',
    'BMCL': 'https://bmclapi2.bangbang93.com/mc/game/version_manifest_v2.json',
}

FORGE_API = {
    'BMCL_MCVERSION': 'https://bmclapi2.bangbang93.com/forge/minecraft',
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
                    res = requests.get(_['url']).json()['downloads']['server']['url']
        case 'Forge':
            versions = [_['version'] for _ in requests.get(f'{FORGE_API["BMCL_MCVERSION"]}/{version}').json()]
            versions.sort(key=lambda x: tuple(int(v) for v in x.split('.')), reverse=True)
            res = f'https://bmclapi2.bangbang93.com/forge/download?mcversion={version}&version={versions[0]}' \
                  '&category=installer&format=jar'
    return res


def install_server(nid):
    # Download
    link = get_link(
        nid.select_serversideChoices[nid.select_serverside.GetSelection()],
        nid.version_list[nid.select_version.GetSelection()]
    )
    header = requests.head(link, allow_redirects=True)
    filesize = header.headers.get('Content-Length')
    if filesize is not None:
        filesize = int(filesize)
    response = requests.get(link, stream=True, allow_redirects=True)
    cs = 512
    dialog = wx.ProgressDialog(nid.trans.gui.window.new_instance.down_progress_title,
                               nid.trans.gui.window.new_instance.down_progress,
                               maximum=filesize,
                               style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_ESTIMATED_TIME)
    dl = 0
    os.mkdir(f'{nid.sc.path}/server')
    os.mkdir(f'{nid.sc.path}/cache')
    with open(f'{nid.sc.path}/cache/installer.jar', 'wb') as f:
        for chunk in response.iter_content(chunk_size=cs):
            f.write(chunk)
            dl += cs
            if dl > filesize:
                dl = filesize
            dialog.Update(dl)
    match nid.select_serversideChoices[nid.select_serverside.GetSelection()]:
        case 'Vanilla':
            shutil.move(f'{nid.sc.path}/cache/installer.jar',
                        f'{nid.sc.path}/server/server.jar')
            nid.sc.config['EXEC_TYPE'] = 'Java'
            nid.sc.config['EXEC'] = '-jar server.jar'
            nid.sc.save_config()
        case 'Forge':
            p = os.popen(f'java -jar {nid.sc.path}/cache/installer.jar --installServer {nid.sc.path}/server/')
            if 'You can delete this installer file now if you wish' in p.read():
                wx.MessageDialog(None, nid.trans.gui.window.new_instance.install_success,
                                 nid.trans.gui.window.new_instance.install_title_success,
                                 wx.OK | wx.ICON_INFORMATION)
                nid.sc.config['EXEC_TYPE'] = 'Shell'
                nid.sc.config['EXEC'] = 'run.bat'
                nid.sc.config.save_config()
            else:
                wx.MessageDialog(None, nid.trans.gui.window.new_instance.install_fail,
                                 nid.trans.gui.window.new_instance.install_title_fail,
                                 wx.OK | wx.ICON_ERROR)


def start_server(sc: data.ServerConfig):
    match sc.config['EXEC_TYPE']:
        case 'Shell':
            subprocess.call(f'start {sc.config["EXEC"]}', cwd=f'{sc.path}/server', shell=True)
        case 'Java':
            subprocess.call(f'start java {sc.config["EXEC"]}', cwd=f'{sc.path}/server', shell=True)


# TEST:
if __name__ == '__main__':
    print(get_serverside_version_list('Spigot'))
