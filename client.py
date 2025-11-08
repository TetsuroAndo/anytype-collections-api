"""Anytype APIクライアント

AnytypeのAPIと通信するためのクライアントクラスです。
"""
import os
from typing import Dict, Any, Optional
import requests


class AnytypeClient:
    """Anytype APIクライアントクラス"""

    def __init__(
        self,
        api_url: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """Anytypeクライアントの初期化

        Args:
            api_url: Anytype APIのURL（環境変数 ANYTYPE_API_URL からも取得可能）
            api_key: APIキー（環境変数 ANYTYPE_API_KEY からも取得可能）
        """
        self.api_url = api_url or os.getenv("ANYTYPE_API_URL", "http://localhost:3030")
        self.api_key = api_key or os.getenv("ANYTYPE_API_KEY")

        if not self.api_key:
            raise ValueError(
                "api_key が必要です。"
                "環境変数 ANYTYPE_API_KEY を設定してください。"
            )

        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Anytype-Version": "2025-05-20",
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """APIリクエストを送信

        Args:
            method: HTTPメソッド（GET, POST, PUT, DELETEなど）
            endpoint: APIエンドポイント
            data: リクエストボディ
            params: クエリパラメータ

        Returns:
            APIレスポンスのJSONデータ

        Raises:
            requests.exceptions.HTTPError: HTTPエラーの場合
        """
        url = f"{self.api_url.rstrip('/')}/{endpoint.lstrip('/')}"

        response = self.session.request(
            method=method,
            url=url,
            json=data,
            params=params,
        )

        # エラーレスポンスの詳細を確認
        if not response.ok:
            error_detail = f"HTTP {response.status_code}"
            try:
                error_body = response.json()
                if isinstance(error_body, dict):
                    error_detail += f": {error_body}"
                else:
                    error_detail += f": {error_body}"
            except Exception:
                error_detail += f": {response.text[:500]}"  # 最初の500文字のみ

            # リクエストデータも含める（デバッグ用）
            if data:
                import json
                try:
                    request_data_str = json.dumps(data, ensure_ascii=False, indent=2)[:1000]
                    error_detail += f"\nリクエストデータ: {request_data_str}"
                except Exception:
                    error_detail += "\nリクエストデータ: (JSON変換失敗)"

            # 詳細情報を含むHTTPErrorを発生
            http_error = requests.exceptions.HTTPError(error_detail, response=response)
            raise http_error

        return response.json()

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GETリクエストを送信"""
        return self._request("GET", endpoint, params=params)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """POSTリクエストを送信"""
        return self._request("POST", endpoint, data=data)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """PUTリクエストを送信"""
        return self._request("PUT", endpoint, data=data)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """PATCHリクエストを送信"""
        return self._request("PATCH", endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETEリクエストを送信"""
        return self._request("DELETE", endpoint)
