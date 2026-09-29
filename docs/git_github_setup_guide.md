# Git / GitHub 環境構築 & プロジェクト登録 仕様書

**対象プロジェクト：無料チャットアプリ（CHAT-APP）**  
**作成日：2025年**  
**対象OS：Windows 10/11**

---

## 目次

1. [Gitのインストール](#1-gitのインストール)
2. [GitHubアカウントの作成](#2-githubアカウントの作成)
3. [GitHubでリポジトリを作成](#3-githubでリポジトリを作成)
4. [ローカルプロジェクトをGitHubに登録](#4-ローカルプロジェクトをgithubに登録)
5. [今後のコード更新手順](#5-今後のコード更新手順)
6. [Renderでインターネット公開（デプロイ）](#6-renderでインターネット公開デプロイ)
7. [プロジェクト情報](#7-プロジェクト情報)

---

## 1. Gitのインストール

### 1-1. Gitをダウンロード
👉 **[https://git-scm.com/download/win](https://git-scm.com/download/win)** を開く

### 1-2. インストーラーを実行
- ダウンロードした `.exe` ファイルをダブルクリック
- すべての設定は **デフォルトのままNext** で進める
- 最後に **「Install」** をクリック

### 1-3. インストール確認
CMDを開いて以下を実行：

```cmd
git --version
```

以下のように表示されれば成功：
```
git version 2.xx.x.windows.x
```

---

## 2. GitHubアカウントの作成

### 2-1. GitHubを開く
👉 **[https://github.com](https://github.com)** をブラウザで開く

### 2-2. アカウント登録
1. **「Sign up」** をクリック
2. 以下を入力：

| 項目 | 内容 |
|------|------|
| Email | 自分のメールアドレス |
| Password | パスワード（8文字以上） |
| Username | ユーザー名（例：pssaikou777-max） |

3. メール認証コードを入力して登録完了

### 2-3. ログイン確認
👉 **[https://github.com](https://github.com)** にログインできればOK

---

## 3. GitHubでリポジトリを作成

### 3-1. 新規リポジトリ作成
1. GitHubにログイン
2. 右上の **「+」ボタン** をクリック
3. **「New repository」** をクリック

### 3-2. リポジトリ情報を入力

| 項目 | 入力内容 |
|------|---------|
| Repository name | `CHAT-APP`（任意の名前） |
| Description | 空白でOK |
| Public / Private | どちらでもOK |
| Initialize this repository | **チェックしない** ← 重要 |

### 3-3. 「Create repository」をクリック

### 3-4. 作成後のURLを控える
作成後の画面に表示されるURLをコピーしておく：
```
https://github.com/ユーザー名/CHAT-APP.git
```

> ✅ 本プロジェクトのURL：
> `https://github.com/pssaikou777-max/CHAT-APP.git`

---

## 4. ローカルプロジェクトをGitHubに登録

### 4-1. CMDを開く
- Windowsキー + R → `cmd` と入力 → Enter

### 4-2. 以下のコマンドを1行ずつ実行

```cmd
cd C:\Users\user\.bob\playground\free_chat_app
```
↑ プロジェクトフォルダに移動

```cmd
git init
```
↑ Gitを初期化

```cmd
git add .
```
↑ 全ファイルをステージに追加

```cmd
git commit -m "first commit"
```
↑ 最初のコミット

```cmd
git remote add origin https://github.com/pssaikou777-max/CHAT-APP.git
```
↑ GitHubリポジトリと接続

```cmd
git branch -M main
```
↑ ブランチ名をmainに設定

```cmd
git push -u origin main
```
↑ GitHubにアップロード

### 4-3. 認証
- ブラウザが開いてGitHubログインを求められる場合がある
- ログインして **「Authentication Succeeded」** が表示されればOK

### 4-4. 成功の確認
以下のような表示が出れば完了：
```
Writing objects: 100% ...
To https://github.com/pssaikou777-max/CHAT-APP.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

---

## 5. 今後のコード更新手順

コードを変更・追加したら以下の4行を実行するだけ：

```cmd
cd C:\Users\user\.bob\playground\free_chat_app
git add .
git commit -m "変更内容のメモ（例：ログイン機能を追加）"
git push
```

### コミットメッセージの例

| 変更内容 | メッセージ例 |
|---------|------------|
| 新機能追加 | `"チャット送信機能を追加"` |
| バグ修正 | `"ログインエラーを修正"` |
| デザイン変更 | `"チャット画面のデザインを更新"` |
| 初回登録 | `"first commit"` |

---

## 6. Renderでインターネット公開（デプロイ）

他のユーザーがブラウザからアクセスできるようにするには、Render（無料クラウドサーバー）にデプロイする。

### 6-1. Renderアカウント作成

1. 👉 **[https://render.com](https://render.com)** を開く
2. **「Get Started for Free」** をクリック
3. **「GitHub でログイン」** を選択
4. GitHubの認証を許可する

---

### 6-2. GitHubとの連携

1. 👉 **[https://github.com/apps/render](https://github.com/apps/render)** を開く
2. **「Configure」** をクリック
3. アカウント **「pssaikou777-max」** を選択
4. **「Only select repositories」** → **「CHAT-APP」** を選択
5. **「Save」** をクリック

---

### 6-3. Web Serviceの作成

1. 👉 **[https://dashboard.render.com/web/new](https://dashboard.render.com/web/new)** を開く
2. **「New Web Service」** をクリック
3. **「pssaikou777-max / CHAT-APP」** を選択して **「Connect」** をクリック

---

### 6-4. サービスの設定

以下の内容を確認・入力する：

| 項目 | 設定値 |
|------|--------|
| Name | `CHAT-APP` |
| Region | `Singapore（Southeast Asia）` |
| Branch | `main` |
| Root Directory | **空白（何も入力しない）** ← 重要 |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `gunicorn wsgi:app --worker-class geventwebsocket.gunicorn.workers.GeventWebSocketWorker --workers 1 --bind 0.0.0.0:$PORT` |
| Plan | **Free（$0/month）** |

> ⚠️ **Root Directory は必ず空白にすること**
> `free_chat_app` と入力するとビルドエラーになる

**「Deploy web service」** をクリック

---

### 6-5. ビルド完了の確認

ログに以下が表示されれば成功：

```
==> Your service is live 🎉
```

公開URLはこちら：
👉 **[https://chat-app-4pnu.onrender.com](https://chat-app-4pnu.onrender.com)**

---

### 6-6. トラブルシューティング（Render）

#### ❌ Root directory does not exist
→ Settingsで **Root Directory を空白** に変更して再デプロイ

#### ❌ Failed to build 'gevent'
→ `requirements.txt` の `gevent` バージョンを `24.11.1` に変更してプッシュ：
```cmd
cd C:\Users\user\.bob\playground\free_chat_app
git add requirements.txt
git commit -m "fix: geventを24.11.1に更新"
git push
```

#### ⚠️ 無料プランの注意事項
- 一定時間アクセスがないと **スリープ状態**になる
- 再アクセス時に **最大50秒** の待ち時間が発生する
- 常時起動が必要な場合は有料プラン（$7/month）へアップグレード

---

## 7. プロジェクト情報

| 項目 | 内容 |
|------|------|
| プロジェクト名 | 無料チャットアプリ |
| ローカルフォルダ | `C:\Users\user\.bob\playground\free_chat_app` |
| GitHubリポジトリURL | https://github.com/pssaikou777-max/CHAT-APP |
| 公開URL（Render） | https://chat-app-4pnu.onrender.com |
| ブランチ | `main` |
| 開発言語 | Python（Flask / FastAPI） |
| Phase 1 | Python Webアプリ |
| Phase 2 | スマホアプリ化（React Native / Flutter / PWA） |

---

## トラブルシューティング

### ❌ `git` コマンドが認識されない
→ Gitがインストールされていない。[手順1](#1-gitのインストール)からやり直す。

### ❌ `git push` でエラーが出る
→ リモートURLが間違っている可能性。以下で確認：
```cmd
git remote -v
```

### ❌ 認証画面が出ない / ログインできない
→ GitHubのユーザー名・パスワードを確認して再試行。

---

*この仕様書は `free_chat_app/docs/git_github_setup_guide.md` に保存されています。*
