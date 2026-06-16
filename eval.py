import json
import sys
from datetime import datetime


def calc_accuracy(pred_file, test_file):
    # 读取预测输出
    with open(pred_file, "r", encoding="utf-8") as f:
        pred_data = json.load(f)
    # 读取原始带标准答案的测试集
    with open(test_file, "r", encoding="utf-8") as f:
        test_data = json.load(f)

    # 构建id -> 预测分类映射
    pred_map = {}
    for item in pred_data:
        pred_map[item["id"]] = item["predicted_category"].strip()

    total = len(test_data)
    correct = 0
    error_list = []  # 用于存放错误样本信息
    for item in test_data:
        tid = item["id"]
        true_label = item["label"]
        pred_label = pred_map.get(tid, "")
        # 取出当前问题文本
        question_text = item["question"]
        if pred_label == true_label:
            correct += 1
        else:
            # 收集错误样本信息
            error_list.append({
                "id": tid,
                "question": question_text,
                "true_label": true_label,
                "pred_label": pred_label
            })

    acc = correct / total
    # 时间戳命名，无变量报错
    time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    err_file_name = f"error_log_{time_str}.json"
    with open(err_file_name, "w", encoding="utf-8") as f:
        json.dump(error_list, f, ensure_ascii=False, indent=2)
    print(f"错误样本已保存至文件：{err_file_name}")

    print(f"总样本数：{total}")
    print(f"预测正确数量：{correct}")
    print(f"错误数量：{len(error_list)}")
    print(f"分类准确率：{acc:.2%}")

    # 新增：打印全部错误详情
    if len(error_list) > 0:
        print("================================错误样本明细=============================")
        for err in error_list:
            print(f"样本ID:{err['id']}")
            print(f"用户问题:{err['question']}")
            print(f"真实标签:{err['true_label']}")
            print(f"模型预测标签:{err['pred_label']}\n")
    else:
        print(" 所有样本预测完全正确，准确率100%! ")
    return acc


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("用法：python eval.py 真实标签文件.json 模型预测文件.json")
    else:
        true_json = sys.argv[1]
        pred_json = sys.argv[2]
        calc_accuracy(pred_json, true_json )
