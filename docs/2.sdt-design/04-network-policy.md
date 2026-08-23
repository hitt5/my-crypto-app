---
type: design
title: ネットワークポリシー（用途 → ネットワーク選択の正本）
tags: [crypto-wealth-os, network, testnet, anvil, policy]
---

# 04 — ネットワークポリシー（Network Policy）

> **テーマ**: dodo Crypto Wealth OS / **theme_id**: `crypto-wealth-os` / **profile**: `crypto` / **作成**: 2026-08-22
> **位置づけ**: 開発・検証・運用で「どのネットワークを使うか」の**唯一の正本**。Charter の原則「不可逆性の低い順に積む」（[`../1.concept/03-approach.md`](../1.concept/03-approach.md) 実装順原理）をネットワーク選択へ適用する。
> **HIL 裁定**: 2026-08-22 — 「用途によるが、スピード重視のローカルを軸にすべき」（ユーザー）。本書はこの裁定の文書化である。

## 1. 原則

1. **Local-first（速度と不可逆性ゼロ）**: 開発・検証の既定ネットワークはローカルテストネット（Anvil）。faucet 不要・資金 mint 自由・即リセット可・オフライン動作（CR-8 local-first と整合）。
2. **不可逆性の昇順**: local → 公開 testnet → mainnet の順でのみ昇格する。逆順の先行使用（いきなり mainnet で試す等）を禁止する。
3. **用途がネットワークを決める**: 「とりあえず Sepolia」「とりあえず mainnet」を禁止し、§2 の写像表で決定論的に選ぶ。
4. **mainnet は Observe（read-only）のみ**: 実行系（送金・署名・Approve）の mainnet 接続は `F-EXECUTION-APPROVE`（P3 / Stage 2 昇格 HIL — CR-2.5）まで凍結。
5. **ネットワーク種別の機械判別**: 設定（`portfolio.json`）の chain エントリは `network_class`（`local-testnet` / `public-testnet` / `mainnet`）を持ち、Action はこれと chain_id で挙動をガードする（例: 資金注入 Action は `local-testnet` 以外を拒否）。

## 2. 用途 → ネットワーク写像（正本）

| 層 | ネットワーク | chain_id | 用途 | 選ぶ理由 / 制約 |
|---|---|---|---|---|
| **L1: ローカル（既定・軸）** | Anvil（Foundry） | 31337 | Action/UI の開発・実 RPC 検証、失敗前提の反復実験、将来の実行系（署名・送金パイプライン）の安全な検証、mainnet fork（`--fork-url`）による実コントラクト相手のシミュレーション | **スピード最優先・不可逆性ゼロ**。資金は `anvil_setBalance` で自由注入。開発ループの既定はここ。起動は `personal.crypto_testnet_ctl` |
| **L2: 公開テストネット** | Sepolia 等 | 11155111 等 | 実ネットワーク遅延・実 P2P 伝播・他者がいる環境・外部連携（faucet / explorer / 第三者コントラクト）の最終確認 | ローカルで再現不能な検証のみに限定。faucet 依存で遅いため既定にしない。**必要になった時点で config に chain 追加のみ**（コード変更不要）。本書改版不要 |
| **L3: Mainnet** | Ethereum mainnet（+ L2） | 1 等 | 本人資産の Observe（残高・価格・Approval の read-only 観測） | 既存 `F-CRYPTO-PORTFOLIO-DASHBOARD` スコープのまま。実行系接続は §1-4 のとおり凍結 |

**迷ったら L1（Anvil）**。L1 で検証できないことが具体的に言えるときだけ L2 へ上げる。

## 3. ローカルテストネット標準構成（Anvil）

| 項目 | 値 |
|---|---|
| 実装 | Foundry Anvil（`brew install foundry`） |
| RPC | `http://127.0.0.1:8545`（localhost 限定 bind — 外部公開しない） |
| chain_id | 31337 |
| 起動/停止/状態 | Personal Action `personal.crypto_testnet_ctl`（op=start/stop/status） |
| 資金注入 | Personal Action `personal.crypto_testnet_fund`（`anvil_setBalance`。`network_class=local-testnet` かつ chain_id=31337 以外は拒否） |
| fork 検証 | `personal.crypto_testnet_ctl` の `fork_url` オプション（mainnet fork）。fork URL は `env://` 間接参照（CR-1.2） |
| 状態ファイル | `.dodoai/personal/data/testnet/anvil.state.json`（PID・起動時刻・設定。Git 非共有） |

### 鍵の扱い（CR-1 との整合）

- Anvil の dev アカウント（公開の well-known ニーモニック由来）は**テスト専用のダミー鍵**であり、CR-1 の「秘密鍵を repo に保存しない」の対象外（公知の値で資産価値ゼロ）。ただし混同防止のため、**dev 秘密鍵をコードにハードコードせず**、fund は `anvil_setBalance`（鍵不要の RPC）を第一手段とする。
- 本人の実 Wallet（dodo sovereign wallet）の鍵・シードは従来どおり一切扱わない。ローカルテストネット上でも本人 Wallet の**アドレス（公開情報）への残高注入と観測のみ**を行う。

## 4. 昇格条件（L1 → L2 → L3）

| 昇格 | 条件 | Gate |
|---|---|---|
| L1 → L2 | L1 で同一シナリオが PASS 済み、かつ L1 で再現できない検証項目を明記 | Issue に検証項目を記録 |
| L2 → L3（Observe） | read-only であること（既存スコープ） | — |
| L3 実行系 | `F-EXECUTION-APPROVE` A02 + Stage 2 昇格 HIL | CR-2.5 / H4 |

## 5. 禁止事項

- 用途写像（§2)を経ない「とりあえず公開ネット」での検証
- 資金注入 Action の `local-testnet` 以外への適用（実装レベルで拒否 — 設定ミス防御）
- Anvil RPC の localhost 外への bind・公開
- dev 秘密鍵のハードコード・本人実鍵のテストネット流用
- mainnet fork URL（API キー入り）の直書き（`env://` のみ）

---

## 改版履歴

| バージョン | 日付 | 内容 |
|---|---|---|
| v0.1.0 | 2026-08-22 | 新設（HIL 裁定の文書化）。用途別 3 層写像・Anvil 標準構成・昇格条件・禁止事項を定義 |
