import subprocess
from subprocess import PIPE


def sample1():
    # dateコマンドを実行して文字列として結果を得る

    cmds_ = [
        ['ls', '--full-time'],
        ['ls'],
        ['ls', '-a', 'work/'],
        ["ls", "-l", "/dev/null"],
        ["ls", "-a"],
    ]

    try:
        for cmd in cmds_:
            proc = subprocess.run(cmd,
                                  shell=False,
                                  stdout=PIPE,
                                  stderr=PIPE,
                                  cwd=r"/work/api",
                                  text=True,
                                  )
            # date = proc.stdout
            # print('STDOUT: {}'.format(date))
            print(f"{'*' * 5} {cmd} {'*' * 5}")
            print(proc.stdout)

    except subprocess.SubprocessError as ex:
        print(ex)


def get_dir_data(cmd, cwd):
    try:
        proc = subprocess.run(cmd,
                              shell=False,
                              stdout=PIPE,
                              stderr=PIPE,
                              cwd=cwd,
                              text=True,
                              )

        return proc.stdout

    except subprocess.SubprocessError as ex:
        print(ex)


def main():
    cmd = ["ls"]
    cwd = r"/work/data"

    result = get_dir_data(cmd=cmd, cwd=cwd)
    files = [i for i in result.split('\n')]
    print(files)
    for file in files:
        if file == 'data.json':
            print(file)
        else:
            print('No data.json: ', file)


if __name__ == '__main__':
    main()
