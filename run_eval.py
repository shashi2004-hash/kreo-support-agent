from agent import ask_agent
from eval_questions import eval_set
import time

def check_pass(answer, expected_keywords):
    """Pass if ANY expected keyword appears in the answer (case-insensitive)"""
    answer_lower = answer.lower()
    return any(keyword.lower() in answer_lower for keyword in expected_keywords)

def run_eval():
    results = []
    passed = 0

    for i, item in enumerate(eval_set, 1):
        question = item["question"]
        expected = item["expected_keywords"]

        answer = ask_agent(question)
        is_pass = check_pass(answer, expected)

        if is_pass:
            passed += 1

        results.append({
            "question": question,
            "answer": answer,
            "expected": expected,
            "pass": is_pass
        })

        status = "PASS" if is_pass else "FAIL"
        print(f"[{i}/{len(eval_set)}] {status} — {question}")
        if not is_pass:
            print(f"    Answer: {answer}")
            print(f"    Expected one of: {expected}")

        time.sleep(0.5)  # small delay to avoid hitting rate limits

    print(f"\n{'='*50}")
    print(f"SCORE: {passed}/{len(eval_set)} ({passed/len(eval_set)*100:.1f}%)")
    print(f"{'='*50}")

    return results

if __name__ == "__main__":
    run_eval()