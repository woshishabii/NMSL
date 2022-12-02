VERSION = 'v-Lithium 0.1 20221129'


class en_US_Translation:
    __lang__ = 'en-US'
    description = 'A Minecraft Server Launcher that helps you set up your server faster'

    class gui:
        title = 'NMSL V-Lithium'

        class menu:
            file = 'File'
            help = 'Help'

        class filemenu:
            new_instance = 'New Server Instance'
            exit = 'Exit'

        class helpmenu:
            about = 'About'

        class statusbar:
            welcome = 'Welcome to NMSL V-Lithium!'
            new_instance = 'Set up a new server instance'
            exit = 'Exit'
            about = 'About NMSL'

        class serverlist:
            servers = 'Servers'

        class homepage:
            start_server = 'Start'

        class window:
            class new_instance:
                title = 'New Server Instance'
                enter_name = 'Name for new instance'
                default_name = 'New Server'
                opendir_label = 'Select Location'
                select_serverside = 'Select Server-side'
                select_version = 'Select Version'
                refresh_metadata = 'Refresh Version List'
                start = 'GO!'
                invalid_name_title = 'Duplicate or Invalid Name'
                invalid_name = 'Invalid Name! Check it!'
                dir_not_exist_title = "Directory Does Not Exist"
                dir_not_exist = "Directory Doesn't Exist, Create?"
                dir_has_file_title = 'Folder is not Empty'
                dir_has_file_config = 'There is a config file in selected Directory, Import?'
                dir_has_file = 'There are file in selected folder, Continue?'
                down_progress_title = 'Downloading...'
                down_progress = 'Downloading'
                install_title_success = 'Success'
                install_title_fail = 'Fail'
                install_success = 'Installation Success'
                install_fail = 'Installation Failed! Check ./installer.jar.log pls'
                install_spigot = 'Spigot is being installed, progress can be checked in the command prompt.'


class zh_CN_Translation:
    __lang__ = 'zh-CN'
    description = '一个简单的MC服务器管理/启动器'

    class gui:
        title = 'NMSL V-Lithium'

        class menu:
            file = '文件'
            help = '帮助'

        class filemenu:
            new_instance = '新建服务器对象'
            exit = '退出'

        class helpmenu:
            about = '关于'

        class statusbar:
            welcome = '欢迎使用NMSL V-Lithium'
            new_instance = '创建新的服务器对象'
            exit = '退出'
            about = '关于NMSL'

        class homepage:
            start_server = '启动'

        class serverlist:
            servers = 'MC服务器'

        class window:
            class about:
                title = '关于 NMSL'
                content = 'Naughty Minecraft Server Launcher\n版本: v-lithium'

            class new_instance:
                title = '新建服务器实例'
                enter_name = '为新实例命名'
                default_name = '新服务器'
                opendir_label = '选择位置'
                select_serverside = '选择服务端'
                select_version = '选择版本'
                refresh_metadata = '刷新版本列表'
                start = 'GO!'
                invalid_name_title = '名称无效'
                invalid_name = '服务器名称重复或无效！'
                dir_not_exist_title = '文件夹不存在'
                dir_not_exist = '文件夹不存在，是否创建？'
                dir_has_file_title = '文件夹非空'
                dir_has_file_config = '文件夹内存在配置文件，导入？'
                dir_has_file = '文件夹非空，仍然使用?'
                down_progress_title = '下载中...'
                down_progress = '下载中'
                install_title_success = '成功'
                install_title_fail = '失败'
                install_success = '安装成功'
                install_fail = '安装失败，请检查./installer.jar.log'
                install_spigot = 'Spigot安装中，可在弹出的命令行中查看进度'


translations = {
    'en-US': en_US_Translation,
    'zh-CN': zh_CN_Translation,
}
