# Copyright (c) 2023 Nordic Semiconductor ASA
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import logging
import os
import shlex

from subprocess import check_output
from pathlib import Path


logger = logging.getLogger(__name__)


def get_imgtool_path() -> Path:
    """Get the path to the imgtool script."""
    zephyr_base = os.getenv("ZEPHYR_BASE") or Path(__file__).parents[4]
    return Path(zephyr_base).parent / "bootloader" / "mcuboot" / "scripts" / "imgtool.py"


def _get_imgtool_sign_base_command(build_dir: Path) -> list[str]:
    """Get imgtool sign command template from the generated build.ninja file."""
    build_ninja = Path(build_dir) / 'build.ninja'
    post_build_prefix = 'POST_BUILD = '
    with open(build_ninja) as f:
        for line in f:
            line = line.strip()
            if not line.startswith(post_build_prefix):
                continue
            post_build_cmd = line[len(post_build_prefix):]
            for command in post_build_cmd.split(' && '):
                if 'imgtool.py sign' not in command or 'zephyr.bin' not in command:
                    continue
                parsed = shlex.split(command)
                sign_idx = parsed.index('sign')
                # Keep command and common imgtool arguments only.
                return parsed[:sign_idx + 1] + parsed[sign_idx + 1:-2]
    raise RuntimeError(f'Cannot find imgtool sign command in: {build_ninja}')


def west_sign_with_imgtool(
        build_dir: Path,
        output_bin: Path | None = None,
        key_file: Path | None = None,
        version: str | None = None,
        timeout: int = 10
):
    """Wrapper method for imgtool-based signing command."""
    command = _get_imgtool_sign_base_command(build_dir)

    # Override dynamic test inputs while preserving board-specific signing args.
    key_indices = [i for i, arg in enumerate(command) if arg == '--key']
    for key_idx in reversed(key_indices):
        del command[key_idx:key_idx + 2]
    if key_file:
        command.extend(['--key', str(key_file)])

    if version and '--version' in command:
        version_idx = command.index('--version')
        command[version_idx + 1] = version

    input_bin = Path(build_dir) / 'zephyr' / 'zephyr.bin'
    output_bin = output_bin or (Path(build_dir) / 'zephyr' / 'zephyr.signed.bin')
    command.extend([str(input_bin), str(output_bin)])

    logger.info(f"CMD: {shlex.join(command)}")
    output = check_output(command, text=True, timeout=timeout)
    logger.debug('OUT: %s' % output)
