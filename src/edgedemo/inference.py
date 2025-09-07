import os
import platform
import subprocess
from pydantic import BaseModel, Field
from typing import Final
BUILD_DIR: Final[str] = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../BitNet/3rdparty/llama.cpp/build"))

class InferenceArgs(BaseModel):
    model: str = Field(..., description="Path to the model file")
    n_predict: int = Field(1, description="Number of tokens to predict")
    threads: int = Field(1, description="Number of threads to use")
    prompt: str = Field(..., description="Prompt to send to the model")
    ctx_size: int = Field(512, description="Context size")
    temperature: float = Field(0.8, description="Sampling temperature")
    conversation: bool = Field(False, description="Enable conversation mode")

class InferenceRunner:
    def __init__(self, args: InferenceArgs) -> None:
        self.args = args
        self.build_dir = BUILD_DIR
        self.main_path = self._get_main_path()

    def _get_main_path(self) -> str:
        if platform.system() == "Windows":
            main_path = os.path.join(self.build_dir, "bin", "Release", "llama-cli.exe")
            if not os.path.exists(main_path):
                main_path = os.path.join(self.build_dir, "bin", "llama-cli")
        else:
            main_path = os.path.join(self.build_dir, "bin", "llama-cli")
        return main_path

    def run(self):
        command = [
            self.main_path,
            '-m', self.args.model,
            '-n', str(self.args.n_predict),
            '-t', str(self.args.threads),
            '-p', self.args.prompt,
            '-ngl', '0',
            '-c', str(self.args.ctx_size),
            '--temp', str(self.args.temperature),
            "-b", "1",
        ]
        if getattr(self.args, 'conversation', False):
            command.append("-cnv")
        subprocess.run(command, check=True)

# Usage:
# runner = InferenceRunner(args)
# runner.run()
