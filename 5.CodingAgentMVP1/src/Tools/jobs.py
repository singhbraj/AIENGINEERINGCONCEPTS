import os
import subprocess
from typing import Any
from pydantic import Field
from pathlib import Path
from dataclasses import UTC, datetime
import contextlib
import signal

@dataclass
class BackgroundJobs:
    pid:int
    command:str
    started_at:str
    log_path:str
    proc:Any = Field(default=None, repr=False)

_Jobs:dict[int, BackgroundJobs] = ()

def register(job:BackgroundJobs)->None:
    _Jobs[job.pid] = job

def get(pid:int)->BackgroundJobs|None:
    return _Jobs.get(pid)

def all_jobs()->list[BackgroundJobs]:
    return list(_Jobs.values())

def remove(pid:int)->BackgroundJobs|None:
    return _Jobs.pop(pid, None)

def is_alive(pid:int)->bool:
    job = get(pid)

    if job is not None and job.proc is not None:
        return job.proc.poll() is None # None means the process is still running

    try:
        os.kill(pid, 0) # 0 means "check if the process exists", do not kill it 
        return True
    except OSError:
        return False


def stop_pid(pid: int) -> str:
    job = get(pid)
    if job is None:
        return f"Error: {pid} is not a job started by this agent."
    if not is_alive(pid):
        if job.proc is not None:
            with contextlib.suppress(ChildProcessError):
                job.proc.wait(timeout=0.1)
        remove(pid)
        return f"Job {pid} was already stopped."
    try:
        os.killpg(pid, signal.SIGTERM)
    except ProcessLookupError:
        remove(pid)
        return f"Job {pid} was already gone."
    except PermissionError as err:
        return f"Error stopping {pid}: {err}"

    if job.proc is not None:
        try:
            job.proc.wait(timeout=1.5)
        except subprocess.TimeoutExpired:
            with contextlib.suppress(ProcessLookupError, PermissionError):
                os.killpg(pid, signal.SIGKILL)
            with contextlib.suppress(subprocess.TimeoutExpired):
                job.proc.wait(timeout=1)
    remove(pid)
    return f"Sent SIGTERM to process group {pid} ({job.command!r})."


def read_log_tail(log_path: Path, *, max_chars: int = 4000) -> str:
    if not log_path.is_file():
        return ""
    text = log_path.read_text(encoding="utf-8", errors="replace")
    if len(text) > max_chars:
        return text[-max_chars:]
    return text


def now_iso() -> str:
    return datetime.now(UTC).isoformat()