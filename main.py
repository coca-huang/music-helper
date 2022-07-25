import logging
import subprocess
import time
from argparse import ArgumentParser
from pathlib import Path

import schedule


def refresh_meta(dst: str | Path):
    logging.debug(f'refresh music meta')
    # get music meta with applescript
    args = ["osascript", "-", f'{Path(dst).absolute()}/']
    kwargs = dict(stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc = subprocess.Popen(args, **kwargs)
    cmd = Path('get-music.applescript').read_text()
    out, err = proc.communicate(cmd.encode('utf-8'))
    out = out.decode('utf-8').rstrip()
    try:
        state, name, artist, a_type = [x.lstrip() for x in out.split(',')]
        logging.info(f'status: {state} | {name} - {artist}')
    except Exception as err:
        logging.error(f'error: {err}')
        return
    # save meta in dst folder
    dst = Path(dst)
    dst.mkdir(parents=True, exist_ok=True)
    _ = [(dst / f'{k}.txt').write_text(v) for k, v in zip(['state', 'name', 'artist'], [state, name, artist])]


if __name__ == "__main__":
    # parser
    parser = ArgumentParser()
    parser.add_argument('--dst', type=str, default='tmp', help='meta output folder')
    parser.add_argument('--log', type=str, default='info', help='log filter level')
    args = parser.parse_args()

    # logging
    logging.basicConfig(level=getattr(logging, args.log.upper()))

    # jobs
    schedule.every(2).seconds.do(refresh_meta, dst=args.dst)

    # scheduler
    while True:
        schedule.run_pending()
        time.sleep(1)
