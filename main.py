"""Anytype APIクライアントのエントリーポイント

コマンドライン引数や環境変数からAPIキーを受け取り、
Anytypeクライアントを初期化してテストします。
"""
import argparse
import sys

from .client import AnytypeClient
from .objects import ObjectManager, AnytypeObject


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
  export ANYTYPE_SPACE_ID=your_space_id
  python -m anytype.main

  # コマンドライン引数でAPIキーを指定
  python -m anytype.main --api-key your_api_key --api-url http://localhost:3030 --space-id your_space_id

  # スペースIDを指定して接続テスト
  python -m anytype.main --api-key your_api_key --space-id your_space_id
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
        "--space-id",
        type=str,
        default=None,
        help="スペースID（環境変数 ANYTYPE_SPACE_ID からも取得可能、指定した場合、接続テストを実行）",
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

        # スペースIDが指定されている場合は接続テスト
        if args.space_id:
            space_id = args.space_id
        else:
            import os
            space_id = os.getenv("ANYTYPE_SPACE_ID")

        if space_id:
            print(f"\n📦 スペースID: {space_id}")
            print("   接続テストを実行中...")

            object_manager = ObjectManager(client=client, space_id=space_id)

            # テストオブジェクトを作成して接続を確認
            try:
                test_object = AnytypeObject(
                    name="接続テスト",
                    body="これは接続テスト用のオブジェクトです。",
                    type_key="page",
                    icon={"emoji": "✅", "format": "emoji"},
                )
                result = object_manager.create_object(test_object)
                print("✅ スペースへの接続に成功しました")
                if "id" in result:
                    print(f"   テストオブジェクトID: {result.get('id')}")
                    # テストオブジェクトを削除（アーカイブ）
                    try:
                        object_manager.delete_object(result["id"])
                        print("   テストオブジェクトを削除しました")
                    except Exception as e:
                        print(f"   警告: テストオブジェクトの削除に失敗しました: {e}")
            except Exception as e:
                print(f"❌ スペースへの接続に失敗しました: {e}")
                sys.exit(1)
        else:
            print("\n💡 ヒント: --space-id を指定するか、環境変数 ANYTYPE_SPACE_ID を設定すると接続テストを実行できます")

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
