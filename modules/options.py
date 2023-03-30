import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--port", type=int, default="7860")
parser.add_argument("--model", type=str, default="model/fp16i8_RWKV-4-Pile-7B-EngChn-test5-20230326")
parser.add_argument("--strategy", type=str, default="cuda fp16i8")
parser.add_argument("--listen", action='store_true', help="launch gradio with 0.0.0.0 as server name, allowing to respond to network requests")

cmd_opts = parser.parse_args()
need_restart = False