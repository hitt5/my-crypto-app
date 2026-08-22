# .dodoai/ ディレクトリ

このディレクトリは、dodoAI SDV-RDプロジェクトのカスタムActions、スキル、および設定を格納します。

## ディレクトリ構造

```
.dodoai/
├── .env                    # 環境変数（APIキー等）※Gitには含めない
├── .env_sample             # 環境変数のサンプル
├── README.md              # このファイル
├── BASE_TEMPLATE/         # Actionテンプレート
├── custom_actions/        # カスタムActions/スキル
│   └── deep-research/    # Deep Researchスキル
└── issue/                 # Issue管理
```

## セットアップ

### 1. 環境変数の設定

```bash
# .env_sampleをコピー
cp .dodoai/.env_sample .dodoai/.env

# .envを編集してAPIキーを設定
vi .dodoai/.env
```

### 2. 必要な環境変数

#### OpenAI API
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

#### Deep Research設定
```bash
DEEP_RESEARCH_MAX_SOURCES=50                    # 最大情報源数
DEEP_RESEARCH_DEFAULT_DEPTH=comprehensive       # デフォルトリサーチ深度
DEEP_RESEARCH_TIMEOUT_SECONDS=3600              # タイムアウト（秒）
DEEP_RESEARCH_MONTHLY_BUDGET_USD=50.00          # 月間予算上限（USD）
```

## カスタムActions/スキル

### Deep Research (`custom_actions/deep-research/`)

OpenAI Deep Research機能を使用した包括的なリサーチとドキュメント生成スキル。

**使い方**:
```bash
# 環境変数を読み込み
source .dodoai/.env

# Agentにプロンプト
"Deep Researchスキルを使って[テーマ]についてリサーチしてください"
```

**詳細**: `custom_actions/deep-research/README.md`を参照

## セキュリティ

### 重要な注意事項

⚠️ **APIキーの管理**:
- `.env`ファイルは**絶対にGitにコミットしない**
- `.gitignore`で除外されています
- APIキーは環境変数として安全に管理

✅ **.env は .gitignore に登録済み**:
```
.dodoai/.env
```

### APIキーの更新

```bash
# 既存のキーを確認
grep OPENAI_API_KEY .dodoai/.env

# キーを更新
vi .dodoai/.env
```

## トラブルシューティング

### Issue: APIキーが読み込まれない

**Solution**:
```bash
# 環境変数を明示的に読み込み
source .dodoai/.env

# 確認
echo $OPENAI_API_KEY
```

### Issue: .envファイルがない

**Solution**:
```bash
# サンプルからコピー
cp .dodoai/.env_sample .dodoai/.env

# APIキーを設定
vi .dodoai/.env
```

## 関連ドキュメント

- **Deep Researchスキル**: `custom_actions/deep-research/README.md`
- **スキル定義**: `custom_actions/deep-research/SKILL.md`
- **Actionテンプレート**: `BASE_TEMPLATE/`
