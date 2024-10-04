from datetime import datetime

from debug import DebugManager as DBM
from debug import init_debug_manager
from env import EnvironmentManager as EM
from github_manager import GitHubManager as GHM
from github_manager import init_github_manager


def main():
    init_github_manager()
    DBM.i('Managers initialized.')

    if not EM.DEBUG_RUN:
        GHM.update_readme()
        GHM.commit_update()
    else:
        GHM.set_github_output()


if __name__ == '__main__':
    init_debug_manager()

    start_time = datetime.now()
    DBM.g('Program execution started at $date.', date=start_time)
    main()
    end_time = datetime.now()
    DBM.g('Program execution finished at $date.', date=end_time)
    DBM.p('Program finished in $time.', time=end_time - start_time)
