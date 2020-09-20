import libtmux
import os
import json
from tqdm import tqdm


with open('config.json', 'r') as config_file:
    config = json.load(config_file)


def stop_all(session_name):
    server = libtmux.Server()
    session = server.find_where({"session_name": session_name})
    session.kill_session()





def start(num_users, base_dir='./'):
    cwd = os.getcwd()
    absolute_path_to_base_dir = os.path.join(cwd, base_dir)
    os.system('cd ' + absolute_path_to_base_dir)
    server = libtmux.Server()
    session = server.new_session(config['session_name'])
    for i in tqdm(range(num_users)):
        window = session.new_window('window_' + str(i), attach=True)
        pane = window.split_window(attach=True)
        env_name = config['env_name_template'] + str(i)
        pane.send_keys('python3 -m venv {}'.format(env_name), enter=True)
        run_jupyter_env_command = \
            "jupyter notebook --ip {ip} --port {port} --NotebookApp.token='{token}' --NotebookApp.notebook_dir='{dir}'" \
                .format(ip=config['ip'], port=config['ports'][i], token='w' + str(i), dir=env_name)
        pane.send_keys(run_jupyter_env_command, enter=True)


def stop(session_name, num):
    server = libtmux.Server()
    session = server.find_where({"session_name": session_name})
    #os.system('jupyter notebook stop {}'.format(config['ports'][num]))
    session.kill_window('window_' + str(num))


#start(3)
#stop('hometask', 0)
#stop_all('hometask')
#remove_old_envs()
