# security-for-developers

「脆弱性のニュースは見るけれど、用語がわからない。システムを作るとき何に気をつければいいのかもわからない」という開発者のための学習サイト「**開発者のためのセキュリティ入門**」です。

サイト：[https://ht-0328.github.io/security-for-developers/](https://ht-0328.github.io/security-for-developers/)

## 何が学べるか

- **用語**：守るもの3つ（機密性・完全性・可用性）、脆弱性・脅威・リスクの関係、ニュースに出る CVE・CVSS・ゼロデイ・PoC・EoL の読み方
- **まずこれだけ**：開発者が守る10のルールと、設計・実装・リリース前・運用の4場面のチェックリスト（Markdown でコピーして PR に貼れる）
- **よくある穴と直し方**：インジェクション・XSS、認証・セッション・認可、暗号化と秘密情報、ライブラリ（サプライチェーン）、インフラ・クラウドの設定、運用とインシデント対応、開発プロセスへの組み込み。危険なコードと安全なコードを並べて示す
- **学ぶ順番**：実務で使えるようになるまでの6段階と、日本語・無料・手を動かせる教材の一覧

## 特徴

- **専門用語には定義を併記**：点線の付いた用語はタップで定義を表示します。各章の「用語の補足」と、全章を横断して検索できる「用語集」も用意しています。
- **分類ごとに色分けしたアイコン**：攻撃＝赤、守り＝緑、データ・部品＝青、人・権限＝紫、運用＝橙。色付きチップの見た目で、色を記憶の手がかりにしています。
- **危険な例と安全な例の対比**：各脆弱性を「何が起きる → なぜ → どう防ぐ → どう確かめる」の順で説明し、コードを NG／OK で並べます。
- **体験コーナー**：CVSS の区分、HTML エスケープ、Cookie 属性、SHA-256、脅威モデリングのワークシートなど、ブラウザだけで試せる小さな道具を各章に置いています。
- **記憶研究に基づく構成**
  - 🧭 各章の冒頭で「理解してほしいこと」と構成を提示
  - 🧠 読み返しではなく想起練習（章末の設問、復習カード）
  - 📅 1日 → 3日 → 7日 → 14日 → 30日 の間隔反復。復習日はサイトが自動で計算します

## ページ構成

```
docs/
├── index.html            トップ（章の一覧と今日の復習）
├── checklist.html        開発者のチェックリスト（設計・実装・リリース前・運用）
├── glossary.html         用語集
├── cards.html            復習カード
├── chapters/
│   ├── study-method.html 学び方：何から、どう学ぶか（最初に読む）
│   ├── 01-overview-terms.html        第1章 セキュリティの全体像と用語
│   ├── 02-ten-rules.html             第2章 まずこれだけ：開発者が守る10のルール
│   ├── 03-injection-xss.html         第3章 入力が原因の脆弱性：インジェクションと XSS
│   ├── 04-auth-session.html          第4章 認証・セッション・認可の脆弱性
│   ├── 05-crypto-secrets.html        第5章 データと秘密情報を守る：暗号化・ハッシュ・鍵
│   ├── 06-dependencies.html          第6章 ライブラリと部品の脆弱性：サプライチェーン
│   ├── 07-infra-cloud.html           第7章 サーバー・クラウド・ネットワークの設定
│   ├── 08-operations-incident.html   第8章 運用：ログ・監視・バックアップ・インシデント対応
│   └── 09-secure-process.html        第9章 開発の流れに組み込む：設計・レビュー・自動検査
└── assets/
    ├── style.css / site.js   共通デザインとスクリプト
    ├── data/chXX.js          各章の復習カードと用語
    └── icons/                分類ごとに色付けしたアイコン（SVG）
        ├── threat/   攻撃・脅威（赤）
        ├── defense/  守り・対策（緑）
        ├── asset/    データ・部品・システム（青）
        ├── people/   人・権限・組織（紫）
        ├── ops/      運用・プロセス・学び（橙）
        └── brand/    ツールのロゴ（白地）
```

## GitHub Pages で公開する手順

`.github/workflows/pages.yml` のワークフローで自動デプロイします。

1. **最初の1回だけ**：GitHub のリポジトリ画面で **Settings → Pages** を開き、**Build and deployment** の Source を「**GitHub Actions**」にする
2. `main` にマージする
3. あとは `main` の `docs/` が変わるたびに自動で公開されます（**Actions** タブの「Deploy to GitHub Pages」から手動実行も可能）
4. 公開先：[https://ht-0328.github.io/security-for-developers/](https://ht-0328.github.io/security-for-developers/)

ローカルで見るときは `docs/index.html` をブラウザで開くだけで OK です。

## 内容を追加するには

- 新しい章：`docs/chapters/` に HTML を追加し、`docs/assets/site.js` の `CHAPTERS` に1行足す
- カード・用語：`docs/assets/data/chXX.js` に追記（新しいファイルを作ったら `cards.html` と `glossary.html` の `<script>` にも追加）
- チェックリストの項目：`docs/checklist.html` の `PHASES` に追記し、`ref` に根拠となる章の節（`id`）を指す
- アイコンを増やす：Lucide の名前を `make_icons.py`（下記）の一覧に足して再生成する。分類ごとの色は同じスクリプトの `CATEGORY_COLOR` で決めている

### アイコンの作り方

アイコンは npm パッケージ [lucide-static](https://www.npmjs.com/package/lucide-static)（線のアイコン）と [simple-icons](https://www.npmjs.com/package/simple-icons)（ブランドロゴ）から、分類ごとの色付きチップ（64×64 の SVG）に加工したものです。生成スクリプトは `tools/make_icons.py` にあります。

```bash
# 1. パッケージを取得して展開する（node は不要。curl と tar だけ）
curl -sL https://registry.npmjs.org/lucide-static/latest | python -c "import json,sys; print(json.load(sys.stdin)['dist']['tarball'])" | xargs curl -sL -o lucide.tgz && mkdir lucide && tar xzf lucide.tgz -C lucide
curl -sL https://registry.npmjs.org/simple-icons/latest | python -c "import json,sys; print(json.load(sys.stdin)['dist']['tarball'])" | xargs curl -sL -o si.tgz && mkdir si && tar xzf si.tgz -C si
# 2. 生成する（出力先 docs/assets/icons）
python -I tools/make_icons.py lucide/package/icons si/package docs/assets/icons
```
