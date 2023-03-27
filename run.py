import os
import openai
import subprocess
import json
import argparse

# DALLE prompt: Futuristic Chiron Shield, pixel art, cyber security


class CodeFile:
    def __init__(self, file_path: str):
        self.file_path = file_path

        with open(file_path, "r") as f:
            self.content = f.read()

        self.results = self.run_semgrep()
        self.finding_count = len(self.results)

    def run_chatgpt(self):
        for result in self.results:
            result["chatgpt"] = self.ask_chatgpt(result["extra"]["lines"])

    def ask_chatgpt(self, content):
        prompt = f"""
        ##### Fix bugs in below code
        
        ### Security issue in code
        {content}
            
        ### Fixed Code
        """

        response = openai.Completion.create(
            model="davinci",
            prompt=prompt,
            temperature=0,
            max_tokens=1250,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["###"],
        )

        return response.choices[0].text

    def run_semgrep(self):
        command = f"semgrep --config=auto {self.file_path} --json"
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE)
        return json.loads(result.stdout.decode("utf-8"))["results"]


def test_file(file_name):
    file = CodeFile(file_name)
    file.run_chatgpt()
    return file


def test_samples():
    samples = []

    # Process files
    for file_name in os.listdir("samples"):
        samples.append(CodeFile(f"samples/{file_name}"))

    for f in samples:
        f.run_chatgpt()

    return samples


def generate_output(results):
    for result in results:
        if result.finding_count == 0:
            print(f"File: {result.file_path}\nNo findings!\n\n")
            continue

        for finding in result.results:
            print("#" * 40)
            CWEs = "\n".join(finding["extra"]["metadata"]["cwe"])
            OWASP = "\n".join(finding["extra"]["metadata"]["owasp"])
            print(f"File path: {result.file_path}\n")
            print(f"Semgrep ID:\n{finding['check_id']}\n")
            print(f"Impact: {finding['extra']['metadata']['impact']}\n")
            print(f"Vulnerable code:\n{finding['extra']['lines']}\n")
            print(f"Semgrep recommendation:\n{finding['extra']['message']}\n")
            print(f"ChatGPT recommended fix:\n{finding['chatgpt'].strip()}\n")
            print(f"CWE:\n{CWEs}\n")
            print(f"OWASP:\n{OWASP}\n")
            print("#" * 40)
            print("\n")


if __name__ == "__main__":
    openai.api_key = os.getenv("OPENAI_API_KEY")
    parser = argparse.ArgumentParser(description="ChironShield")

    parser.add_argument("-t", help="Test Sample files", action="store_true")
    parser.add_argument("-f", help="file")

    args = parser.parse_args()

    if args.t:
        generate_output(test_samples())
    if args.f:
        f = test_file(args.f)
        generate_output([f])
