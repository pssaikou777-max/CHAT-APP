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
6. [プロジェクト情報](#6-プロジェクト情報)

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

## 6. プロジェクト情報

| 項目 | 内容 |
|------|------|
| プロジェクト名 | 無料チャットアプリ |
| ローカルフォルダ | `C:\Users\user\.bob\playground\free_chat_app` |
| GitHubリポジトリURL | https://github.com/pssaikou777-max/CHAT-APP |
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
