import json

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
    for item in test_data:
        tid = item["id"]
        true_label = item["label"]
        pred_label = pred_map.get(tid, "")
        if pred_label == true_label:
            correct += 1

    acc = correct / total
    print(f"总样本数：{total}")
    print(f"预测正确数量：{correct}")
    print(f"分类准确率：{acc:.2%}")
    return acc

if __name__ == "__main__":
    calc_accuracy("base_output.json", "task1_test_samples.json")