import json

import requests

class DatabaseAccessTool:
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

    def execute_sql(self, sql, limit=None):
        url = f"{self.base_url}/query"
        data = {
            "sql": sql
        }
        if limit is not None:
            data["limit"] = limit
        response = requests.post(url, headers=self.headers, json=data)
        return response.json()