import logging
import os
import subprocess
import sys
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
    """ current work directory """
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


def test(in_dir_, file_id=None):
    try:
        cwd = os.getcwd()
        print(cwd)

        os.chdir(in_dir_)

        cmd = "pwd"
        subprocess.call(cmd)

        os.chdir(cwd)
        subprocess.call(cmd)

        print('::: done :::')

    except FileNotFoundError as ex:
        logging.error(msg=ex)
        export_parameter_file(file_id=file_id, tr_id=10, skip_flag=True)
        # sys.exit(211)


def export_parameter_file(dir_='param', file_id=None, tr_id=None, skip_flag=None):
    """ export Parameter File """
    with open(f"{dir_}/{file_id}.params", 'w') as f:
        print(f"file_id={file_id}", file=f)
        print(f"tr_id={tr_id}", file=f)
        print(f"skip_flag={skip_flag}", file=f)


if __name__ == '__main__':
    # main()
    test('/bin', file_id='RK0099')
    test('/work', file_id='RK0098')
    test('/work', file_id='RK0001')
    test('/boot/', file_id='RK0002')
    test('mnt/fsx', file_id='RK0003')
    test('/work/try/mnt/fsx', file_id='RK0004')
    test('mnt/fsx', file_id='RK0005')
