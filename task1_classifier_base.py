#!/usr/bin/env python3
"""
客服 FAQ 自动分类脚本
用途：对用户发来的问题进行自动分类，分配到对应的客服组
"""

import json
from openai import OpenAI

# API 配置
client=OpenAI(
	api_key="个人LLM平台API KEY",
                base_url="模型服务商兼容模式接口地址"
)
MODEL = "qwen-plus"
def classify_question(question: str) -> str:
    """对单条用户问题进行分类"""
    prompt = f"""你是专业电商客服文本分类助手，严格按照下方规则执行分类：
可选分类仅有6类：退款退货、物流查询、账号问题、商品咨询、投诉建议、其他

分类判定规则：
1. 退款退货：用户要求退款、退货、换货、咨询退款进度；
2. 物流查询：查询包裹位置、派送状态、快递地址修改；
3. 账号问题：登录、密码、账号冻结、绑定手机号相关；
4. 商品咨询：询问商品规格、尺码、材质、库存、参数；
5. 投诉建议：商品质量不满、客服投诉、平台功能建议；
6. 其他：闲聊、无意义短句、无法归入以上五类内容。

强制输出要求：
1. 若一句话同时包含多个诉求，**只选取用户最核心诉求对应的单一类别**；
2. 仅输出类别名称，禁止逗号、顿号、解释、多余文字、符号；
3. 不允许同时输出两个及以上分类标签。

用户问题：{question}
仅输出单一分类名称："""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    result = response.choices[0].message.content.strip()
    return result


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

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"分类完成，共处理 {len(results)} 条问题")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("用法: python classifier.py <输入文件> <输出文件>")
        sys.exit(1)

    batch_classify(sys.argv[1], sys.argv[2])
