# FinanceFast_Bus

***
成绩验证分数: 42.36分

成绩验证时间: 2024年12月18日 9:00 PM

完整运行时长: 3小时12分钟

完整运行Token消耗: GLM-4-Plus 620万 Tokens
***

## 队伍简介

FinanceFast_Bus 提供频繁、可靠且迅速的服务，帮助您在不同地点之间转移金融资源，就如同您的财务的公共公交系统一样。

作者： **公交车的轮子转啊转**

## 方案简介

本方案通过多轮交互式对话，结合GLM模型与数据库技术，实现高效、精准的命名实体识别、SQL语句生成与优化、数据库查询，以及结果的交互式处理。旨在为用户提供快速、灵活且智能化的问答体验。

### 方案亮点

1. **多轮交互，精准回答**：支持与模型进行多轮对话，动态生成SQL语句并查询数据库，逐步优化查询，直至输出完整、准确的答案。
2. **SQL简单优化**：自动识别并优化SQL语句，解决常见的`date`格式不匹配等问题，提高查询效率与兼容性。
3. **召回列名和中文注释简单优化**：在召回列名和中文注释时进行智能化处理，确保结果更加贴合用户需求，减少理解障碍。

## 主要功能

### 1. **问答流程**

- 读取用户问题，结合数据库内容与表结构，生成相应SQL语句进行查询。
- 支持多轮对话交互，在每一步都对结果进行验证和后续查询。

### 2. **SQL优化**

- 对生成的SQL语句进行优化，包括日期格式化、条件处理等，使SQL语句在指定数据库中能高效运行。
- 支持对语句进行语法检查，防止执行错误。

### 3. **命名实体识别**

- 自动识别问题中的关键实体，包括公司名称、基金名称、证券代码等。
- 根据实体类型映射到数据库表，生成适配的SQL查询语句。

### 4. **数据查询与结果输出**

- 提供对数据库的查询接口，通过SQL获取表数据，并进行后续处理。
- 输出标准化、结构化的JSON格式结果，并可直接保存为文件。

---

## 运行复现

1. 运行以下命令以安装所需依赖：

```bash
pip install -r requirements.txt
```

2. 打开run.ipynb文件。确保所有依赖库已正确安装。依次运行文件中的各个单元格，系统将自动完成问答流程。运行完成后，程序会将结果保存到
   **`result.json`** 文件中。如果你只想运行部分问题。可以调整`start_idx`和`end_idx`的值。具体位置相见 jupyter
   notebook最后一个代码块。

3. 本方案均使用题目数据，因此，你可以在主仓库的`assets`文件夹找到。

## 核心功能详解

### **1. 工具函数**

项目内实现了一系列工具函数，主要功能包括：

- **`create_chat_completion`**：与模型交互，生成对话结果。
- **`replace_date_with_day`**：优化SQL语句中的日期格式。
- **`filter_table_comments`**：从数据库表注释中提取与问题相关的内容。
- **`process_company_name` / `process_code`**：根据公司名称或代码查询数据库。

### **2. 多轮交互**

- 项目支持与模型多轮交互，每轮生成SQL语句并查询数据库，直到获取完整答案。
- 提供 `run_conversation_until_complete` 函数，实现动态查询。

### **3. 命名实体识别**

- 使用示例和模板对问题中的关键实体进行抽取。
- 支持公司名称（中英文全称、简称）、基金名称、证券代码等多种实体类型。

---

## 输出结果示例

设置参数:
```
start_idx = 63 # 起始问题索引
end_idx = 64 # 结束问题索引
```

**输入问题**：

```json
[
  {
    "tid": "tttt----64",
    "team": [
      {
        "id": "tttt----64----36-4-1",
        "question": "最新更新的2021年度报告中，机构持有无限售流通A股数量合计最多的公司简称是？"
      },
      {
        "id": "tttt----64----36-4-2",
        "question": "在这份报告中，该公司机构持有无限售流通A股比例合计是多少，保留2位小数？"
      },
      {
        "id": "tttt----64----36-4-3",
        "question": "该公司前十大股东持股比例合计是多少？"
      }
    ]
  }
]
```

**输出结果**：

```json
[
  {
    "tid": "tttt----64",
    "team": [
      {
        "id": "tttt----64----36-4-1",
        "question": "最新更新的2021年度报告中，机构持有无限售流通A股数量合计最多的公司简称是？",
        "answer": "公司简称 帝尔激光"
      },
      {
        "id": "tttt----64----36-4-2",
        "question": "在这份报告中，该公司机构持有无限售流通A股比例合计是多少，保留2位小数？",
        "answer": "机构持有无限售流通A股比例合计(%) 10.1309"
      },
      {
        "id": "tttt----64----36-4-3",
        "question": "该公司前十大股东持股比例合计是多少？",
        "answer": "Top10StockholdersProp 64.51"
      }
    ]
  }
]
```

---

## 注意事项

1. **数据库连接**：确保数据库接口可用，并正确设置访问令牌（`ACCESS_TOKEN`、`ZhipuAI_API_KEY`）。
2. **SQL语句优化**：确保 SQL 语句符合目标数据库的语法规则。

---

## 写在最后

`命名实体识别` 函数得到了 **@躺躺不想动了** 老师的大力支持，**@开源专家zR** 对代码进行了辛勤整理，在此表示衷心的感谢。

希望我的开源方案能够成为大家的一点灵感和参考。如果其中有不足之处，还请多多包涵！

衷心期望它能为大家的夺冠之路增添一丝助力！💪✨

希望你喜欢这个项目！ 😊



