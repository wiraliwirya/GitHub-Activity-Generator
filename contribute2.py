#!/usr/bin/env python3

import argparse
import os
import sys
import logging
from datetime import datetime, timedelta
from random import randint, gauss
from subprocess import Popen, PIPE, DEVNULL
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger(__name__)


def run(commands: list[str], capture: bool = False) -> tuple[int, str, str]:
    try:
        proc = Popen(
            commands,
            stdout=PIPE if capture else DEVNULL,
            stderr=PIPE if capture else DEVNULL
        )
        stdout, stderr = proc.communicate()
        return (
            proc.returncode,
            stdout.decode().strip() if stdout else '',
            stderr.decode().strip() if stderr else ''
        )
    except FileNotFoundError:
        log.error(f"Perintah tidak ditemukan: {commands[0]}")
        sys.exit(1)
    except Exception as e:
        log.error(f"Error: {e}")
        return (-1, '', str(e))


def git_is_available() -> bool:
    code, _, _ = run(['git', '--version'], capture=True)
    return code == 0


def message(date: datetime) -> str:
    return date.strftime('Contribution: %Y-%m-%d %H:%M')


def contributions_per_day(args: argparse.Namespace) -> int:
    max_c = min(max(args.max_commits, 1), 20)
    n = int(abs(gauss(max_c / 2, max_c / 4))) + 1
    return max(1, min(n, max_c))


def contribute(date: datetime) -> bool:
    log_file = Path(os.getcwd()) / 'commits.txt'
    try:
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(message(date) + '\n')

        code, _, err = run(['git', 'add', 'commits.txt'], capture=True)
        if code != 0:
            log.warning(f"git add gagal: {err}")
            return False

        date_str = date.strftime('%Y-%m-%d %H:%M:%S')
        code, _, err = run([
            'git', 'commit', '-q',
            '-m', message(date),
            '--date', date_str
        ], capture=True)

        if code != 0:
            log.warning(f"git commit gagal: {err}")
            return False

        return True

    except IOError as e:
        log.error(f"Gagal menulis commits.txt: {e}")
        return False


def setup_repository(directory: str, args: argparse.Namespace) -> bool:
    path = Path(directory)

    if path.exists():
        log.info(f"Folder '{directory}' sudah ada, menggunakannya.")
    else:
        try:
            path.mkdir(parents=True)
            log.info(f"Folder '{directory}' dibuat.")
        except OSError as e:
            log.error(f"Gagal membuat folder: {e}")
            return False

    os.chdir(directory)

    code, _, _ = run(['git', 'init', '-b', 'main'], capture=True)
    if code != 0:
        run(['git', 'init'], capture=True)
        run(['git', 'checkout', '-b', 'main'], capture=True)

    if args.user_name:
        run(['git', 'config', 'user.name', args.user_name])
    if args.user_email:
        run(['git', 'config', 'user.email', args.user_email])

    log_file = Path('commits.txt')
    if not log_file.exists():
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write('# Contribution log\n\n')
        run(['git', 'add', 'commits.txt'])
        run(['git', 'commit', '-m', 'init: add contribution log'])
        log.info("commits.txt dibuat dan commit awal selesai.")

    return True


def push_to_remote(repository: str) -> bool:
    log.info("Mengatur remote origin...")
    run(['git', 'remote', 'remove', 'origin'], capture=True)

    code, _, err = run(['git', 'remote', 'add', 'origin', repository], capture=True)
    if code != 0:
        log.error(f"Gagal menambah remote: {err}")
        return False

    run(['git', 'branch', '-M', 'main'])

    log.info("Push ke GitHub...")
    try:
        proc = Popen(['git', 'push', '-u', 'origin', 'main'])
        proc.wait()
        if proc.returncode != 0:
            log.error("Push gagal. Pastikan token/SSH sudah benar dan repo sudah dibuat di GitHub.")
            return False
        return True
    except KeyboardInterrupt:
        log.warning("\nPush dibatalkan.")
        sys.exit(0)


def print_progress(current: int, total: int, commit_count: int, date: datetime):
    bar_len = 30
    filled = int(bar_len * current / total)
    bar = '#' * filled + '-' * (bar_len - filled)
    pct = current / total * 100
    print(
        f"\r  [{bar}] {pct:5.1f}%  |  "
        f"{date.strftime('%Y-%m-%d')}  |  "
        f"{commit_count} commits",
        end='', flush=True
    )


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)

    if not git_is_available():
        log.error("Git tidak ditemukan. Install git dulu: https://git-scm.com")
        sys.exit(1)

    curr_date = datetime.now()

    if args.repository:
        start = args.repository.rfind('/') + 1
        end = args.repository.rfind('.')
        if end == -1:
            end = len(args.repository)
        directory = args.repository[start:end] or f'repo-{curr_date.strftime("%Y%m%d%H%M%S")}'
    else:
        directory = f'repository-{curr_date.strftime("%Y-%m-%d-%H-%M-%S")}'

    if args.days_before < 0 or args.days_after < 0:
        log.error("days_before dan days_after tidak boleh negatif.")
        sys.exit(1)

    original_dir = os.getcwd()
    if not setup_repository(directory, args):
        sys.exit(1)

    start_date = curr_date.replace(hour=20, minute=0, second=0, microsecond=0) \
                 - timedelta(days=args.days_before)
    total_days = args.days_before + args.days_after

    log.info(f"Range  : {start_date.strftime('%Y-%m-%d')} s/d "
             f"{(start_date + timedelta(total_days)).strftime('%Y-%m-%d')}")
    log.info(f"Setting: {args.frequency}% frekuensi | max {min(args.max_commits, 20)} commits/hari")
    log.info(f"Output : commits.txt (README.md tidak disentuh sama sekali)")
    print()

    commit_count = 0
    skipped_days = 0

    for i in range(total_days):
        day = start_date + timedelta(days=i)
        print_progress(i + 1, total_days, commit_count, day)

        if args.no_weekends and day.weekday() >= 5:
            skipped_days += 1
            continue

        if randint(0, 100) >= args.frequency:
            continue

        n_commits = contributions_per_day(args)
        for m in range(n_commits):
            commit_time = day + timedelta(minutes=m * randint(5, 30))
            if contribute(commit_time):
                commit_count += 1

    print()
    print()
    log.info(f"Selesai. Total: {commit_count} commits | {skipped_days} hari di-skip.")

    if args.repository:
        success = push_to_remote(args.repository)
        if success:
            print('\nSUKSES! Cek profil GitHub kamu.')
        else:
            print('\nCommit sudah dibuat tapi push gagal. Coba manual:')
            print(f'  cd {directory} && git push -u origin main')
    else:
        print(f'\nCommit berhasil dibuat di folder: {directory}')
        print('Tambahkan remote : git remote add origin <URL>')
        print('Lalu push        : git push -u origin main')

    os.chdir(original_dir)


def arguments(argsval):
    parser = argparse.ArgumentParser(
        description='GitHub Contribution Graph Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh:
  python contribute.py -r https://github.com/username/repo.git
  python contribute.py -r https://github.com/username/repo.git -db 365 -mc 5 -fr 70
  python contribute.py -db 180 -nw -mc 3
        """
    )
    parser.add_argument('-nw', '--no_weekends', action='store_true', default=False,
                        help="Jangan commit di akhir pekan")
    parser.add_argument('-mc', '--max_commits', type=int, default=10,
                        help="Maksimal commit per hari (default: 10, maks: 20)")
    parser.add_argument('-fr', '--frequency', type=int, default=80,
                        help="Persentase hari yang di-commit (default: 80)")
    parser.add_argument('-r', '--repository', type=str,
                        help="URL remote repository GitHub")
    parser.add_argument('-un', '--user_name', type=str,
                        help="git config user.name")
    parser.add_argument('-ue', '--user_email', type=str,
                        help="git config user.email")
    parser.add_argument('-db', '--days_before', type=int, default=365,
                        help="Hari ke belakang dari hari ini (default: 365)")
    parser.add_argument('-da', '--days_after', type=int, default=0,
                        help="Hari ke depan dari hari ini (default: 0)")
    return parser.parse_args(argsval)


if __name__ == '__main__':
    main()
