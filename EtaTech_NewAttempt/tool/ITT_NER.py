import json
import os

from EtaTech_NewAttempt.utils.chat_tool import ChatTool

access_token = 'df4f19f600214b9da99db3265023df0a'
model_air = "glm-4-air"
api_key_air = '2f252bef2ec446719359d4457574fee1.JOfVYlXzamOs2Qwc'
model_zero = "glm-zero-preview"
api_key_zero = "bb39dea715524cce99af3e9e9a5d8be0.tbf9mU4sw3BUnerD"
# question_data_path = r'../../data/question.json'
question_data_path = r'../../data/question_test.json'
out_data_base_path = '../out/data/'
table_description_file = os.path.join(out_data_base_path, "table_description.json")

# 读取table_description.json文件
table_description = json.load(open(table_description_file, 'r', encoding='utf-8'))

chat = ChatTool(api_key_zero, model_zero)

def get_table_list(questions):
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
    table_list = ["LC_StockArchives","LC_NameChange","LC_Business","LC_ExgIndustry","LC_ExgIndChange","LC_IndustryValuation","LC_IndFinIndicators","LC_COConcept","LC_ConceptList","LC_SuppCustDetail","LC_SHTypeClassifi","LC_MainSHListNew","LC_SHNumber","LC_Mshareholder","LC_ActualController","LC_ShareStru","LC_StockHoldingSt","LC_ShareTransfer","LC_ShareFP","LC_ShareFPSta","LC_Buyback","LC_BuybackAttach","LC_LegalDistribution","LC_NationalStockHoldSt","CS_ForeignHoldingSt","LC_AShareSeasonedNewIssue","LC_ASharePlacement","LC_Dividend","LC_CapitalInvest","CS_StockCapFlowIndex","CS_TurnoverVolTecIndex","CS_StockPatterns","QT_DailyQuote","QT_StockPerformance","LC_SuspendResumption","LC_BalanceSheetAll","LC_IncomeStatementAll","LC_CashFlowStatementAll","LC_IntAssetsDetail","LC_MainOperIncome","LC_OperatingStatus","LC_AuditOpinion","LC_Staff","LC_RewardStat","LC_Warrant","LC_Credit","LC_SuitArbitration","LC_EntrustInv","LC_Regroup","LC_MajorContract","LC_InvestorRa","LC_InvestorDetail","LC_ESOP","LC_ESOPSummary","LC_TransferPlan","LC_SMAttendInfo","HK_EmployeeChange","HK_StockArchives","CS_HKStockPerformance","US_CompanyInfo","US_DailyQuote","MF_FundArchives","MF_FundProdName","MF_InvestAdvisorOutline","MF_Dividend","LC_ViolatiParty","LC_IndexBasicInfo","LC_IndexComponent","LC_InstiArchive","SecuMain","HK_SecuMain","CT_SystemConst","QT_TradingDayNew","LC_AreaCode","PS_EventStru","US_SecuMain","PS_NewsSecurity"]
    select_table_answer = chat.send_message()
    select_table_list = []
    for table in table_list:
        if table in select_table_answer:
            select_table_list.append(table)
    return select_table_list


def get_question_sql(team):
    questions = ""
    for question_i in team:
        questions+=question_i["question"]
    table_json_list = get_table_list(questions)
    print(table_json_list)

if __name__ == '__main__':
    question_data = json.load(open(question_data_path, 'r', encoding='utf-8'))
    for i in question_data:
        get_question_sql(i["team"])