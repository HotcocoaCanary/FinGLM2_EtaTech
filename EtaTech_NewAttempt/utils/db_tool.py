import requests

class DBTool:
    def __init__(self, access_token):
        self.base_url = "https://comm.chatglm.cn/finglm2/api"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

    def get_databases(self):
        """获取所有数据库信息"""
        url = f"{self.base_url}/databases"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def execute_sql(self, sql, limit=10):
        url = f"{self.base_url}/query"
        data = {
            "sql": sql,
            "limit": limit
        }
        if limit is not None:
            data["limit"] = limit
        response = requests.post(url, headers=self.headers, json=data)
        response_json = response.json()
        return response_json

    def execute_sql_list(self, sql_list):
        data = []
        for sql in sql_list:
            result = self.execute_sql(sql)
            data.append(result)
        return data