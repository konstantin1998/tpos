#! /usr/bin/env python3

import argparse
import json
from env1.interface import start, stop, stop_all
import os

def remove_old_envs(env_name_template, base_dir='./'):
    cwd = os.getcwd()
    absolute_path_to_base_dir = os.path.join(cwd, base_dir)
    os.system('cd ' + absolute_path_to_base_dir)
    os.system('rm -r {env}*'.format(env=env_name_template))


def setup(args):
    with open('config.json', 'r') as config_file:
        configuration = json.load(config_file)
    configuration['relative_path'] = args.working_dir
    configuration['ports'] = args.ports
    with open('config.json', 'w') as config_file:
        json.dump(configuration, config_file)

    start(len(args.ports), args.working_dir)


def stop_envs(args):
    pass


def stop_env(args):
    print('args:', vars(args))
    print('ports:', args.ports)
    print('length:', len(vars(args)))


parser = argparse.ArgumentParser(description='start and stop jupyter notebooks')
subparsers = parser.add_subparsers(title='subcommands',
                                   description='valid subcommands',
                                   help='description')

start_parser = subparsers.add_parser('start', help='start envs')
start_parser.add_argument('--working_dir', type=str, help='directory for python envs', default='./')
start_parser.add_argument('ports', nargs='+', type=int)
start_parser.set_defaults(func=setup)

stop_parser = subparsers.add_parser('stop', help='start envs')
stop_parser.add_argument('session_name', type=str, help='session to select')
stop_parser.add_argument('num', type=int, help='selected env')
stop_parser.set_defaults(func=stop_env)

stop_all_parser = subparsers.add_parser('stop_all', help='stop all envs and kill session')
stop_all_parser.add_argument('session_name', type=str, help='selected session')
stop_all_parser.set_defaults(func=stop_envs)

if __name__ == '__main__':
    args = parser.parse_args()
    if not vars(args):
        parser.print_usage()
    else:
        args.func(args)