import json
import os

from EtaTech_NewAttempt.utils.chat_tool import ChatTool

# model_air = "glm-4-air"
# api_key_air = '2f252bef2ec446719359d4457574fee1.JOfVYlXzamOs2Qwc'
model = "glm-zero-preview"
api_key = "bb39dea715524cce99af3e9e9a5d8be0.tbf9mU4sw3BUnerD"
chat = ChatTool(api_key, model)


def get_table_and_schema_list(questions, table_description):
    """
    根据问题和表描述，获取可能使用到的数据表名称和数据库名称列表。

    参数:
    questions (str): 问题内容。
    table_description (list): 表描述信息列表。

    返回:
    tuple: 包含选中的表名称列表和选中的数据库名称列表。
    """
    messages = [
        {
            "role": "system",
            "content": "你是一个自然语言分析大师，你需要根据数据库表信息，仔细研读每个表的注意事项，里面包含表与表之间的关联关系。"
                       "随后根据问题，分析问题意图，并识别出问题中的实体，最后返回所有和问题有关联的所有数据表"
                       "表信息如下：\n" + str(table_description)
        },
        {
            "role": "user",
            "content": "根据数据表描述给我当前问题可能使用到的所有数据表名称"
                       "问题如下：\n" + questions
        }
    ]
    chat.set_message(messages)
    schema_list = ["USStockDB", "PublicFundDB", "IndexDB", "InstitutionDB", "HKStockDB", "CreditDB", "ConstantDB",
                   "AStockShareholderDB", "AStockOperationsDB", "AStockMarketQuotesDB", "AStockIndustryDB",
                   "AStockFinanceDB", "AStockEventsDB", "AStockBasicInfoDB"]
    table_list = ["LC_StockArchives", "LC_NameChange", "LC_Business", "LC_ExgIndustry", "LC_ExgIndChange",
                  "LC_IndustryValuation", "LC_IndFinIndicators", "LC_COConcept", "LC_ConceptList", "LC_SuppCustDetail",
                  "LC_SHTypeClassifi", "LC_MainSHListNew", "LC_SHNumber", "LC_Mshareholder", "LC_ActualController",
                  "LC_ShareStru", "LC_StockHoldingSt", "LC_ShareTransfer", "LC_ShareFP", "LC_ShareFPSta", "LC_Buyback",
                  "LC_BuybackAttach", "LC_LegalDistribution", "LC_NationalStockHoldSt", "CS_ForeignHoldingSt",
                  "LC_AShareSeasonedNewIssue", "LC_ASharePlacement", "LC_Dividend", "LC_CapitalInvest",
                  "CS_StockCapFlowIndex", "CS_TurnoverVolTecIndex", "CS_StockPatterns", "QT_DailyQuote",
                  "QT_StockPerformance", "LC_SuspendResumption", "LC_BalanceSheetAll", "LC_IncomeStatementAll",
                  "LC_CashFlowStatementAll", "LC_IntAssetsDetail", "LC_MainOperIncome", "LC_OperatingStatus",
                  "LC_AuditOpinion", "LC_Staff", "LC_RewardStat", "LC_Warrant", "LC_Credit", "LC_SuitArbitration",
                  "LC_EntrustInv", "LC_Regroup", "LC_MajorContract", "LC_InvestorRa", "LC_InvestorDetail", "LC_ESOP",
                  "LC_ESOPSummary", "LC_TransferPlan", "LC_SMAttendInfo", "HK_EmployeeChange", "HK_StockArchives",
                  "CS_HKStockPerformance", "US_CompanyInfo", "US_DailyQuote", "MF_FundArchives", "MF_FundProdName",
                  "MF_InvestAdvisorOutline", "MF_Dividend", "LC_ViolatiParty", "LC_IndexBasicInfo", "LC_IndexComponent",
                  "LC_InstiArchive", "SecuMain", "HK_SecuMain", "CT_SystemConst", "QT_TradingDayNew", "LC_AreaCode",
                  "PS_EventStru", "US_SecuMain", "PS_NewsSecurity"]
    select_table_answer = chat.send_message()
    select_table_list = []
    select_schema_list = []
    for table in table_list:
        if table in select_table_answer or table.lower() in select_table_answer:
            select_table_list.append(table)
    for table_description_i in table_description:
        for table in select_table_list:
            if table_description_i["表名"] == table and table_description_i["数据库名"] not in select_schema_list:
                select_schema_list.append(table_description_i["数据库名"])
    for schema in schema_list:
        if schema in select_table_answer or schema.lower() in select_table_answer:
            select_schema_list.append(schema)
    return select_table_list, select_schema_list


def recall_data(team, table_description_path, data_dict_path):
    """
    根据团队问题和表描述路径，获取相关的表详细数据和问题内容。

    参数:
    team (list): 问题列表。
    table_description_path (str): 表描述文件路径。
    data_dict_path (str): 数据字典路径。

    返回:
    tuple: 包含选中的表描述信息列表、表详细数据列表和问题内容。
    """
    table_description_file = os.path.join(table_description_path)
    table_description = json.load(open(table_description_file, 'r', encoding='utf-8'))
    questions = ""
    for question_i in team:
        questions += question_i["question"]
    table_list, schema_list = get_table_and_schema_list(questions, table_description)
    # 获取表详细数据
    table_dict = []
    select_table_description = []
    for schema_list_i in schema_list:
        data = json.load(open(data_dict_path + "/" + schema_list_i + ".json", 'r', encoding='utf-8'))
        table_dict.append(data)
    for table_list_i in table_list:
        for table_description_i in table_description:
            if table_description_i["表名"] == table_list_i:
                select_table_description.append(table_description_i)
    # 根据table_list和schema_list生成sql
    return select_table_description, table_dict, questions
