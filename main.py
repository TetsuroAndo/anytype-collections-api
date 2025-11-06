"""Anytype APIクライアントのエントリーポイント

コマンドライン引数や環境変数からAPIキーを受け取り、
Anytypeクライアントを初期化してテストします。
"""
import argparse
import sys

from .client import AnytypeClient
from .table import TableManager, TableRow


def main():
    """メイン処理"""
    parser = argparse.ArgumentParser(
        description="Anytype APIクライアントのエントリーポイント",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  # 環境変数からAPIキーを読み込む
  export ANYTYPE_API_KEY=your_api_key
  export ANYTYPE_API_URL=http://localhost:3030
  python -m anytype.main

  # コマンドライン引数でAPIキーを指定
  python -m anytype.main --api-key your_api_key --api-url http://localhost:3030

  # テーブルIDを指定して接続テスト
  python -m anytype.main --api-key your_api_key --table-id your_table_id
        """.strip()
    )

    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Anytype APIキー（環境変数 ANYTYPE_API_KEY からも取得可能）",
    )
    parser.add_argument(
        "--api-url",
        type=str,
        default=None,
        help="Anytype API URL（環境変数 ANYTYPE_API_URL からも取得可能、デフォルト: http://localhost:3030）",
    )
    parser.add_argument(
        "--table-id",
        type=str,
        default=None,
        help="テーブルID（指定した場合、接続テストを実行）",
    )

    args = parser.parse_args()

    try:
        # クライアントを初期化
        client = AnytypeClient(
            api_url=args.api_url,
            api_key=args.api_key,
        )

        print("✅ Anytypeクライアントの初期化に成功しました")
        print(f"   API URL: {client.api_url}")

        # テーブルIDが指定されている場合は接続テスト
        if args.table_id:
            print(f"\n📊 テーブルID: {args.table_id}")
            print("   接続テストを実行中...")

            table_manager = TableManager(client=client, table_id=args.table_id)

            # テーブルの行を取得して接続を確認
            try:
                result = table_manager.get_rows(limit=1)
                print("✅ テーブルへの接続に成功しました")
                if "rows" in result:
                    print(f"   行数: {len(result.get('rows', []))}件（最初の1件のみ取得）")
            except Exception as e:
                print(f"❌ テーブルへの接続に失敗しました: {e}")
                sys.exit(1)
        else:
            print("\n💡 ヒント: --table-id を指定すると接続テストを実行できます")

    except ValueError as e:
        print(f"❌ エラー: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 予期しないエラーが発生しました: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
