# -*- coding: utf-8 -*-

import subprocess
from typing import Optional


class Runner:
    """Runs application code
    """

    def __init__(self, script: str):
        """
        Args:
            script (str): Path to an executable script
        """
        super().__init__()

        self.script = script
        self.p: Optional[subprocess.Popen[bytes]] = None
        self.running = False

    def run(self) -> bool:
        """Runs the application

        Returns:
            bool: Returns true if the script was started successfully
        """
        if self.script != None:
            try:
                self.p = subprocess.Popen(self.script)
                self.running = True
            except (FileNotFoundError, PermissionError):
                return False

        return True

    def stop(self):
        """Stops the application
        """
        if self.p:
            self.p.terminate()
        self.running = False
