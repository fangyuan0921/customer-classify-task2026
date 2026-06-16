#!/usr/bin/env python3
"""
客服 FAQ 自动分类脚本
用途：对用户发来的问题进行自动分类，分配到对应的客服组
"""

import json
import os
import sys
from openai import OpenAI


# 新增：读取外部 prompt文件，统一系统提示词
with open("task1_prompt_v3.md", "r",
encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()
# API 配置
client = OpenAI(
    api_key=os.getenv("LLM_API_KEY"),
    base_url=os.getenv("LLM_BASE_URL")
)
MODEL = "qwen-plus"


def classify_question(question: str) -> str:
    """对单条用户问题进行分类"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"用户问题:{question}"}
    ]
    # 调用模型，增加temperature=0消除随机错判
    completion = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.0
    )
    return completion.choices[0].message.content.strip()


def batch_classify(input_file: str, output_file: str):
    """批量分类"""
    with open(input_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)
    results = []
    for item in questions:
        question = item['question']
        category = classify_question(question)
        results.append({
            'id': item['id'],
            'question': question,
            'predicted_category': category
        })

    with open(output_file, 'w', encoding='utf-8') as write_f:
        json.dump(results, write_f, ensure_ascii=False, indent=2)

    print(f"分类完成，共处理 {len(results)} 条问题")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("用法: python classifier.py <输入文件> <输出文件>")
        sys.exit(1)
    batch_classify(sys.argv[1], sys.argv[2])
