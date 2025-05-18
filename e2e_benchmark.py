import os
import sys
import signal
import platform
import argparse
import subprocess

def run_command(command, shell=False):
    """Run a system command and ensure it succeeds."""
    try:
        subprocess.run(command, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running command: {e}")
        sys.exit(1)

def run_benchmark():
    build_dir = "build"
    if platform.system() == "Windows":
        benchmark_path = os.path.join(build_dir, "bin", "Release", "llama-benchmark.exe")
        if not os.path.exists(benchmark_path):
            benchmark_path = os.path.join(build_dir, "bin", "llama-benchmark.exe")
    else:
        benchmark_path = os.path.join(build_dir, "bin", "llama-benchmark")
    
    command = [
        f'{benchmark_path}',
        '-m', args.model,
        '-c', str(args.ctx_size),
        '-t', str(args.threads),
        '-n', str(args.n_predict),
        '-ngl', '0',
        '--temp', str(args.temperature),
        '--benchmark', str(args.benchmark),
    ]
    
    if args.prompt:
        command.extend(['-p', args.prompt])
    
    print(f"Starting benchmark with model {args.model}")
    run_command(command)

def signal_handler(sig, frame):
    print("Ctrl+C pressed, exiting...")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser(description='Run end-to-end benchmark')
    parser.add_argument(
        "-m",
        "--model",
        type=str,
        help="Path to model file (default: models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf)",
        required=False,
        default="models/BitNet-b1.58-2B-4T/ggml-model-i2_s.gguf",
    )
    parser.add_argument("-p", "--prompt", type=str, help="System prompt for the model", required=False)
    parser.add_argument("-n", "--n-predict", type=int, help="Number of tokens to predict", required=False, default=4096)
    parser.add_argument("-t", "--threads", type=int, help="Number of threads to use", required=False, default=2)
    parser.add_argument("-c", "--ctx-size", type=int, help="Size of the context window", required=False, default=2048)
    parser.add_argument("--temperature", type=float, help="Temperature for sampling", required=False, default=0.8)
    parser.add_argument("--benchmark", type=int, help="Number of benchmark iterations", required=False, default=10)
    
    args = parser.parse_args()
    run_benchmark()
