#!/usr/bin/env python3

import shutil
import psutil
from network import *


def check_disk_usage(disk):
    """Verifies theres enough disk space"""
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20

def check_cpu_usage():
    """Verifies theres enough cpu"""
    usage = psutil.cpu_percent(1)
    return usage < 75

#if else statement for enough disk or cpu
if not check_disk_usage ('/') or not check_cpu_usage():
    print("Error")
elif check_localhost() and check_connectivity():
    print("Everything is Okay")
else:
    print("Network Checks failed")
