# anytype-api - Anytype API操作ライブラリ

AnytypeのAPIを通じてテーブル操作を行う再利用可能なPythonライブラリです。

## 特徴

- ✅ Anytype APIとの通信機能
- ✅ テーブル行の作成・更新・削除・取得
- ✅ バッチ処理対応
- ✅ Upsert機能（追加または更新）
- ✅ 再利用可能なモジュール設計
- ✅ git submoduleとして利用可能

## インストール

### git submoduleとして使用

```bash
# メインプロジェクトで
git submodule add <repository-url> anytype
git submodule update --init --recursive
```

### 依存関係のインストール

```bash
pip install requests
# または
uv add requests
```

## 使用方法

### 基本的な使用例

```python
from anytype import AnytypeClient, TableManager, TableRow

# クライアントの作成
client = AnytypeClient(
    api_url="http://localhost:3030",
    api_key="your_api_key"
)

# テーブルマネージャーの作成
table_manager = TableManager(client=client, table_id="your_table_id")

# 行の作成
row = TableRow(fields={
    "name": "テストプロジェクト",
    "description": "説明文"
})
table_manager.create_row(row)
```

### 環境変数からの設定読み込み

```python
import os
os.environ["ANYTYPE_API_URL"] = "http://localhost:3030"
os.environ["ANYTYPE_API_KEY"] = "your_api_key"

# 環境変数から自動的に読み込まれる
client = AnytypeClient()
```

サポートされている環境変数:
- `ANYTYPE_API_URL`: API URL（デフォルト: `http://localhost:3030`）
- `ANYTYPE_API_KEY`: APIキー（必須）

### バッチ処理

```python
# 複数行を一度に追加
rows = [
    TableRow(fields={"name": "プロジェクト1"}),
    TableRow(fields={"name": "プロジェクト2"}),
    TableRow(fields={"name": "プロジェクト3"}),
]
table_manager.create_rows(rows)
```

### Upsert機能

```python
# 一意なフィールドを指定して追加または更新
row = TableRow(fields={
    "id": "unique_id",
    "name": "更新されたプロジェクト名"
})
table_manager.upsert_row(row, unique_fields=["id"])
```

### 行の取得

```python
# すべての行を取得
result = table_manager.get_rows()

# ページネーション
result = table_manager.get_rows(limit=10, offset=0)

# フィルター付き
result = table_manager.get_rows(filters={"status": "active"})
```

### コマンドラインエントリーポイント

このライブラリはコマンドラインから直接実行可能なエントリーポイントを提供しています。

#### 基本的な使用方法

```bash
# 環境変数からAPIキーを読み込む
export ANYTYPE_API_KEY=your_api_key
export ANYTYPE_API_URL=http://localhost:3030
python -m anytype.main

# コマンドライン引数でAPIキーを指定
python -m anytype.main --api-key your_api_key --api-url http://localhost:3030

# テーブルIDを指定して接続テストを実行
python -m anytype.main --api-key your_api_key --table-id your_table_id
```

#### オプション

- `--api-key`: Anytype APIキー（環境変数 `ANYTYPE_API_KEY` からも取得可能）
- `--api-url`: Anytype API URL（環境変数 `ANYTYPE_API_URL` からも取得可能、デフォルト: `http://localhost:3030`）
- `--table-id`: テーブルID（指定した場合、接続テストを実行）

#### ヘルプの表示

```bash
python -m anytype.main --help
```

#### パッケージインストール後の使用

パッケージをインストールすると、`anytype`コマンドが直接使用可能になります：

```bash
# パッケージをインストール
pip install -e .

# コマンドラインから直接実行
anytype --api-key your_api_key --table-id your_table_id
```

## APIリファレンス

### AnytypeClient

Anytype APIクライアントクラス。

#### 初期化

```python
client = AnytypeClient(
    api_url: Optional[str] = None,  # 環境変数 ANYTYPE_API_URL からも取得可能
    api_key: Optional[str] = None   # 環境変数 ANYTYPE_API_KEY からも取得可能（必須）
)
```

#### メソッド

- `get(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`: GETリクエスト
- `post(endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`: POSTリクエスト
- `put(endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`: PUTリクエスト
- `delete(endpoint: str) -> Dict[str, Any]`: DELETEリクエスト

### TableManager

Anytypeテーブル管理クラス。

#### 初期化

```python
manager = TableManager(
    client: AnytypeClient,
    table_id: str
)
```

#### メソッド

- `create_row(row: TableRow) -> Dict[str, Any]`: 行を追加
- `create_rows(rows: List[TableRow]) -> Dict[str, Any]`: 複数行を追加
- `get_rows(limit: Optional[int] = None, offset: Optional[int] = None, filters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]`: 行を取得
- `update_row(row_id: str, row: TableRow) -> Dict[str, Any]`: 行を更新
- `delete_row(row_id: str) -> Dict[str, Any]`: 行を削除
- `upsert_row(row: TableRow, unique_fields: Optional[List[str]] = None) -> Dict[str, Any]`: 行を追加または更新

### TableRow

テーブル行のデータクラス。

#### 初期化

```python
row = TableRow(fields: Dict[str, Any])
```

#### メソッド

- `to_dict() -> Dict[str, Any]`: APIリクエスト用の辞書形式に変換

## モジュール構造

```
anytype/
├── __init__.py          # パブリックAPIのエクスポート
├── client.py           # AnytypeClientクラス
├── table.py            # TableManagerとTableRowクラス
├── main.py             # コマンドラインエントリーポイント
├── pyproject.toml      # パッケージ設定
└── README.md           # このファイル
```

## ライセンス

このライブラリは再利用可能なモジュールとして設計されています。
