"""
xlsclients - list client applications connected to the X server

Uses python-xlib, https://pypi.org/project/python-xlib/ to communicate with the X server.
"""
from dataclasses import dataclass
from Xlib.display import Display
from Xlib.ext import res as XRes


def query_client_id(display, wid):
    specs = [{"client": wid, "mask": XRes.LocalClientPIDMask}]
    r = display.res_query_client_ids(specs)
    for id in r.ids:
        if id.spec.client > 0 and id.spec.mask == XRes.LocalClientPIDMask:
            for value in id.value:
                return value
    return None


def get_process_name(pid: int) -> str:
    try:
        with open(f"/proc/{pid}/comm", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return "unknown"


@dataclass
class ProcessInfo:
    pid: int
    name: str


def get_process_info(display: Display, client: int) -> ProcessInfo:
    pid = query_client_id(display, client)
    if pid is None:
        return ProcessInfo(-1, "unknown")

    process_name = get_process_name(pid)
    return ProcessInfo(pid, process_name)


def main():
    display = Display()
    clients = display.res_query_clients().clients
    for client in clients:
        process_info = get_process_info(display, client.resource_base)
        print(f"{process_info.name} ({process_info.pid})")


if __name__ == "__main__":
    main()
