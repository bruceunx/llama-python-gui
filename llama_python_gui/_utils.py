import subprocess


def check_gpu_availability() -> bool:
    try:
        subprocess.check_output('nvidia-smi')
        return True
    except Exception:
        return False
