"""Core hermetic code sandbox isolator implementation."""
import os
import shutil
import subprocess
import sys
import tempfile
from typing import Dict, Optional

class SandboxExecutionResult:
    def __init__(self, exit_code: int, stdout: str, stderr: str):
        self.exit_code = exit_code
        self.stdout = stdout
        self.stderr = stderr
        self.is_success = (exit_code == 0)

class HermeticSandbox:
    def __init__(self, timeout_seconds: float = 5.0):
        self.timeout = timeout_seconds

    def execute_code(self, script_body: str, env_vars: Optional[Dict[str, str]] = None) -> SandboxExecutionResult:
        temp_dir = tempfile.mkdtemp(prefix="agent_sandbox_")
        script_path = os.path.join(temp_dir, "run.py")

        try:
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_body)

            # Hermetic minimal environment
            safe_env = {"PYTHONPATH": "", "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")}
            if env_vars:
                safe_env.update(env_vars)

            proc = subprocess.run(
                [sys.executable, script_path],
                cwd=temp_dir,
                env=safe_env,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            return SandboxExecutionResult(proc.returncode, proc.stdout, proc.stderr)
        except subprocess.TimeoutExpired:
            return SandboxExecutionResult(-1, "", "Execution timed out")
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
