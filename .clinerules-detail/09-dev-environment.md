え# 開発環境

> **TODO: プロジェクトに合わせてカスタマイズしてください**

## 起動
```bash
{プロジェクトの起動コマンドを記載}    # 全サービス起動
{プロジェクトの停止コマンドを記載}     # 停止
```
初回: {プロジェクトの初期セットアップコマンドを記載}

## サービス一覧

| サービス | ポート | 起動コマンド |
|---------|-------|------------|
| Backend API | `:8000` | `{your-command}` |
| Frontend Dev | `:3000` | `{your-command}` |

## テスト実行
```bash
# Backend テスト
{your-test-command}

# Frontend テスト
{your-test-command}

# カバレッジ確認
{your-coverage-command}
```

## ヘルスチェック
```bash
curl -s http://localhost:8000/health && echo " ✅ Backend OK" || echo " ❌ Backend DOWN"
curl -s http://localhost:3000/ && echo " ✅ Frontend OK" || echo " ❌ Frontend DOWN"
```
