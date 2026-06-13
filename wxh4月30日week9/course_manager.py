import random

print("Week 9：数据分析与搜索算法基础")
print("--------------------------------")

# 1. 统计分析演示
print("1. 数据统计分析")

scores = [78, 85, 92, 67, 88, 95, 73]

average = sum(scores) / len(scores)
highest = max(scores)
lowest = min(scores)

print(f"成绩列表: {scores}")
print(f"平均分: {average:.2f}")
print(f"最高分: {highest}")
print(f"最低分: {lowest}")

print("--------------------------------")

# 2. 二分查找演示
print("2. 二分查找演示")

numbers = sorted(random.sample(range(1, 100), 15))
target = numbers[7]

left = 0
right = len(numbers) - 1
position = -1

while left <= right:
    mid = (left + right) // 2

    if numbers[mid] == target:
        position = mid
        break
    elif numbers[mid] < target:
        left = mid + 1
    else:
        right = mid - 1

print(f"有序数组: {numbers}")
print(f"目标值: {target}")
print(f"找到位置: {position}")

print("--------------------------------")

# 3. 字符频率统计
print("3. 字符频率统计")

text = "artificial intelligence"

frequency = {}

for char in text:
    if char != " ":
        frequency[char] = frequency.get(char, 0) + 1

print(f"文本: {text}")
print("统计结果:")

for key, value in sorted(frequency.items()):
    print(f"{key}: {value}")

print("--------------------------------")
print("程序结束")