# -*- coding:utf-8 -*-
import sys

from modules.overwrites import *
from modules.config import *
from ChuanhuChatbot import (
    demo,
    reload_javascript,
)


if __name__ == "__main__":
    reload_javascript()

    if len(sys.argv) >= 2:
        _server_port = int(sys.argv[1])
    else:
        _server_port = server_port

    demo.title += " for Glow"

    demo.queue(concurrency_count=CONCURRENT_COUNT).launch(
        blocked_paths=["config.json"],
        server_name=server_name,
        server_port=_server_port,
        share=share,
        auth=None,
        favicon_path="./web_assets/favicon.ico",
        inbrowser=not dockerflag,  # 禁止在docker下开启inbrowser
    )
