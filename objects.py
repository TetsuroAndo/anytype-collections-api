"""Anytypeオブジェクト操作モジュール

Anytypeのオブジェクトを操作するためのモジュールです。
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from .client import AnytypeClient


@dataclass
class AnytypeObject:
    """Anytypeオブジェクトのデータクラス"""
    name: str
    body: str = ""
    type_key: str = "page"
    icon: Optional[Dict[str, Any]] = None
    properties: Optional[List[Dict[str, Any]]] = None

    def to_dict(self) -> Dict[str, Any]:
        """APIリクエスト用の辞書形式に変換"""
        data = {
            "name": self.name,
            "body": self.body,
            "type_key": self.type_key,
        }
        if self.icon:
            data["icon"] = self.icon
        if self.properties:
            data["properties"] = self.properties
        return data


class ObjectManager:
    """Anytypeオブジェクト管理クラス"""

    def __init__(self, client: AnytypeClient, space_id: str):
        """オブジェクトマネージャーの初期化

        Args:
            client: Anytypeクライアント
            space_id: スペースID
        """
        self.client = client
        self.space_id = space_id

    def create_object(self, obj: AnytypeObject) -> Dict[str, Any]:
        """オブジェクトを作成

        Args:
            obj: 作成するオブジェクトデータ

        Returns:
            APIレスポンス
        """
        endpoint = f"v1/spaces/{self.space_id}/objects"
        return self.client.post(endpoint, data=obj.to_dict())

    def get_object(self, object_id: str) -> Dict[str, Any]:
        """オブジェクトを取得

        Args:
            object_id: オブジェクトID

        Returns:
            APIレスポンス
        """
        endpoint = f"v1/spaces/{self.space_id}/objects/{object_id}"
        return self.client.get(endpoint)

    def update_object(
        self,
        object_id: str,
        obj: AnytypeObject,
    ) -> Dict[str, Any]:
        """オブジェクトを更新

        Args:
            object_id: オブジェクトID
            obj: 更新するオブジェクトデータ

        Returns:
            APIレスポンス
        """
        endpoint = f"v1/spaces/{self.space_id}/objects/{object_id}"
        return self.client.patch(endpoint, data=obj.to_dict())

    def delete_object(self, object_id: str) -> Dict[str, Any]:
        """オブジェクトを削除（アーカイブ）

        Args:
            object_id: オブジェクトID

        Returns:
            APIレスポンス
        """
        endpoint = f"v1/spaces/{self.space_id}/objects/{object_id}"
        return self.client.delete(endpoint)

    def create_objects(self, objects: List[AnytypeObject]) -> List[Dict[str, Any]]:
        """複数のオブジェクトを作成

        Args:
            objects: 作成するオブジェクトデータのリスト

        Returns:
            APIレスポンスのリスト
        """
        results = []
        for obj in objects:
            try:
                result = self.create_object(obj)
                results.append(result)
            except Exception as e:
                # エラーが発生した場合は例外を再発生させるか、エラー情報を含める
                results.append({"error": str(e), "object": obj.name})
        return results
