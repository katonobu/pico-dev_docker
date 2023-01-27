import os

class EnvUtil():
    def __init__(self):
        self.isWindowsOs = os.name == 'nt'
        
        # https://techracho.bpsinc.jp/morimorihoge/2017_03_06/36503
        self.isRunningOnDocker = os.path.isfile('/.dockerenv')

        # https://zenn.dev/ryuu/scraps/a683aee48a2e70
        self.isRunningOnWsl = os.path.isfile('/proc/sys/fs/binfmt_misc/WSLInterop')

        # https://endy-tech.hatenablog.jp/entry/how_venv_works_in_python
        self.pythonOnVenv = os.getenv('VIRTUAL_ENV') is not None

    def __repr__(self):
        kws = [f"{key}={value!r}" for key, value in self.__dict__.items()]
        return "{}({})".format(type(self).__name__, ", ".join(kws))

if __name__ == '__main__':
    print(EnvUtil())
