class en_US_Translation:
    __lang__ = 'en-US'

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

        class window:
            class about:
                title = 'About NMSL'
                content = 'Naughty Minecraft Server Launcher\nVersion: v-lithium'

            class new_instance:
                title = 'New Server Instance'


class zh_CN_Translation:
    __lang__ = 'zh-CN'

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

        class window:
            class about:
                title = '关于 NMSL'
                content = 'Naughty Minecraft Server Launcher\n版本: v-lithium'

            class new_instance:
                title = '新建服务器实例'


translations = {
    'en-US': en_US_Translation,
    'zh-CN': zh_CN_Translation,
}
