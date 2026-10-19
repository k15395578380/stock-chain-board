import sys
from run_golden import AGENT

def main():
    if len(sys.argv) < 2:
        print("用法: python scripts/ask.py \"你的问题\"")
        sys.exit(1)
    query = " ".join(sys.argv[1:])
    result = AGENT.query(query)
    print(result.get("text", ""))
    if result.get("segments"):
        print(f"\n涉及环节: {', '.join(result['segments'])}")
    if result.get("sources"):
        print(f"来源数: {len(result['sources'])}")

if __name__ == "__main__":
    main()