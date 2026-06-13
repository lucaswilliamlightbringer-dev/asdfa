# 📝 Week 9 数据分析与搜索算法基础实验

姓名：王昕昊（Wang Xinhao）
学校：Shinhan University 国际学院 软件工程专业
课程名称：AI Robotics & Vision System
实验日期：2026年4月30日

---

# 🇨🇳 实验内容概述（Experiment Overview）

本周实验主要围绕 Python 基础编程、数据处理以及经典搜索算法展开。

通过编写 Python 程序，实现了数据统计分析、二分查找算法以及字符频率统计等功能，进一步熟悉了 Python 基础语法、数据结构以及算法实现过程。

整个实验涉及：

* Python 基础编程
* 数据统计分析
* 列表（List）操作
* 字典（Dictionary）应用
* 二分查找（Binary Search）
* 字符频率统计
* VS Code 开发环境

---

# 1. 数据统计分析实验

## 实验过程

首先创建成绩列表，并利用 Python 内置函数进行统计分析。

实验数据如下：

```python
scores = [78, 85, 92, 67, 88, 95, 73]
```

程序分别计算：

```python
average = sum(scores) / len(scores)
highest = max(scores)
lowest = min(scores)
```

统计内容包括：

* 平均分
* 最高分
* 最低分

---

## 实验结果

成功获得：

* 平均成绩
* 最高成绩
* 最低成绩

验证了 Python 在数据分析中的基本应用能力。

---

# 2. 二分查找算法实验

## 实验过程

本部分实现经典的 Binary Search（二分查找）算法。

首先随机生成并排序数据：

```python
numbers = sorted(random.sample(range(1, 100), 15))
```

随后设置目标值：

```python
target = numbers[7]
```

通过不断缩小搜索区间完成目标查找。

核心思想：

* 获取中间位置
* 判断目标大小
* 缩小搜索范围
* 直到找到目标值

---

## 实验结果

程序能够：

* 自动生成有序数组
* 快速定位目标元素
* 输出目标所在位置

实验验证了二分查找的高效搜索特性。

---

# 3. 字符频率统计实验

## 实验过程

利用 Python 字典结构统计字符串中每个字符出现的次数。

测试字符串：

```python
text = "artificial intelligence"
```

程序通过遍历字符串完成统计：

```python
frequency[char] = frequency.get(char, 0) + 1
```

最终输出所有字符及对应出现次数。

---

## 实验结果

成功统计：

* 字母出现次数
* 字符频率分布
* 文本特征信息

进一步掌握了字典在数据统计中的实际应用。

---

# 4. 实验收获与总结

## 学习内容

通过本次实验掌握了：

* Python 基础语法应用
* List 数据结构使用
* Dictionary 数据结构使用
* 数据统计分析方法
* Binary Search 实现原理
* 字符频率统计方法

---

## 实验总结

本次实验通过多个基础案例，将数据分析与算法应用进行了结合。

在实验过程中，不仅提高了 Python 编程能力，也进一步理解了数据结构与算法的重要性。通过对数据统计、搜索算法以及字符分析的实践，为后续学习人工智能、机器人视觉以及更复杂的数据处理技术打下了良好的基础。

---

# 🇺🇸 English Summary

## Data Analysis

A Python program was developed to perform basic statistical analysis on a dataset.

The program successfully calculated:

* Average value
* Maximum value
* Minimum value

This exercise demonstrated fundamental data processing techniques in Python.

---

## Binary Search Algorithm

A binary search algorithm was implemented using a sorted list.

The system successfully:

* Generated ordered data
* Located target values efficiently
* Returned the target index

The experiment verified the efficiency of Binary Search.

---

## Character Frequency Analysis

A dictionary-based character counting program was created.

The program analyzed:

* Character occurrences
* Frequency distribution
* Text statistics

This exercise strengthened understanding of Python dictionaries and data analysis.

---

## Experiment Outcome

The experiment successfully demonstrated:

* Python programming fundamentals
* Statistical analysis
* Binary Search implementation
* Dictionary operations
* Character frequency counting

These skills provide a solid foundation for future studies in robotics, AI, and computer vision.

---

# 🇰🇷 한국어 요약

## 데이터 분석

Python을 이용하여 데이터 통계 분석 프로그램을 구현하였다.

프로그램은 다음 항목을 계산하였다.

* 평균값
* 최대값
* 최소값

이를 통해 Python 데이터 처리 기초를 학습하였다.

---

## 이진 탐색 알고리즘

정렬된 배열을 이용하여 Binary Search 알고리즘을 구현하였다.

프로그램은 다음 기능을 수행하였다.

* 정렬 데이터 생성
* 목표값 탐색
* 인덱스 반환

이진 탐색의 효율성을 확인할 수 있었다.

---

## 문자 빈도 분석

Python Dictionary를 사용하여 문자열 내 문자 출현 빈도를 분석하였다.

분석 내용:

* 문자 개수
* 빈도 분포
* 텍스트 통계

Dictionary 자료구조 활용 능력을 향상시킬 수 있었다.

---

## 최종 결과

본 실험을 통해 다음 내용을 학습하였다.

* Python 기초 프로그래밍
* 데이터 통계 분석
* Binary Search 알고리즘
* Dictionary 활용
* 문자 빈도 분석

향후 인공지능, 로봇공학 및 컴퓨터 비전 분야 학습의 기초를 다질 수 있었다.

---

<img src="img/data_analysis.png" alt="data analysis" width="700">

<img src="img/binary_search.png" alt="binary search" width="700">

<img src="img/character_frequency.png" alt="character frequency" width="700">
