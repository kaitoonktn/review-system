"""
レビュー生成ツール v3（CLI版）
外部APIなし・Python標準ライブラリのみで動作

【v3 追加機能】
- スタイル選択：丁寧 / カジュアル / SNS用
- 出力フォーマット選択：Amazon風 / 楽天風 / ブログ風
- StyleTemplate dataclass でスタイルをデータとして管理
- スタイル x フォーマット が独立して自由に組み合わせ可能（3x3=9通り）
"""

import random
from datetime import datetime
from dataclasses import dataclass


# ============================================================
# ユーティリティ
# ============================================================

def pick(options: list) -> str:
    return random.choice(options)

def pick_no_repeat(options: list, last: str) -> str:
    choices = [o for o in options if o != last]
    return random.choice(choices) if choices else random.choice(options)

def clean(text: str) -> str:
    return text.rstrip("。．.、,，!！?？")


# ============================================================
# スタイルテンプレート定義
# ============================================================

@dataclass
class StyleTemplate:
    """1スタイル分のテンプレート群をまとめたデータクラス"""
    name: str
    title_templates: list
    intro_backgrounds: list
    first_impressions: list
    good_lead_ins: list
    connectors: list
    endings_positive: list
    concern_leads: list
    concern_endings: list
    outro_templates: list
    star_ratings: list
    usage_periods: list


# ──────────────────────────────────────
# スタイル① 丁寧レビュー
# ──────────────────────────────────────
STYLE_FORMAL = StyleTemplate(
    name="丁寧レビュー",
    title_templates=[
        "【{name}】{period}使用した率直な評価（{stars}）",
        "{name} 購入レビュー｜実際に{period}使ってわかったこと",
        "「{name}」は買いでしょうか？{period}の使用経験をもとにご報告します",
        "【{stars}評価】{name}を{period}使い続けた正直な感想",
    ],
    intro_backgrounds=[
        "以前から気になっておりましたが、今回ご縁があり購入することができました。",
        "複数の商品を比較検討した結果、こちらを選ぶことにいたしました。",
        "知人から勧められたことがきっかけで、実際に試してみることにしました。",
        "口コミや評判を丁寧に確認した上で、購入を決断いたしました。",
    ],
    first_impressions=[
        "届いた際の梱包はていねいで、開封時から品質の高さが伝わってまいりました。",
        "実物を手にした第一印象は「想像以上にしっかりした造りだ」というものでした。",
        "外観の質感・仕上げともに、価格帯を考えると非常に満足のいくものでした。",
        "手に取った瞬間から、細部へのこだわりが感じられました。",
    ],
    good_lead_ins=[
        "実際に使用してみて、特に評価したい点として、",
        "購入前の期待を上回っていたと感じたのが、",
        "日常的に使用する中で、とりわけ重宝しているのが、",
        "使い続けることでその真価がわかってきたのが、",
    ],
    connectors=[
        "また、",
        "さらに、",
        "加えて申し上げると、",
        "もう一点ご紹介しますと、",
        "その他にも、",
        "付け加えますと、",
    ],
    endings_positive=[
        "という点で、これは大変助かっております。",
        "という部分は、期待以上の水準であったと感じています。",
        "という点は、長く愛用したいと思わせる大きな理由のひとつです。",
        "というのは、実際に使ってみて初めてわかった魅力でした。",
        "という部分は、日々の使用において確かな満足感をもたらしてくれます。",
    ],
    concern_leads=[
        "一方で、率直に申し上げると、若干気になった点もございます。",
        "完璧かと問われると、惜しいと感じる部分も正直なところあります。",
        "改善を望む点として、ひとつ挙げるとすれば、",
    ],
    concern_endings=[
        "という点は、今後の改善に期待したいところです。",
        "という部分は、使用上やや不便を感じました。",
        "という点は、検討材料としてお伝えしておく必要があるかと思います。",
    ],
    outro_templates=[
        "総合的に評価いたしますと、「{name}」は十分におすすめできる商品です。細部の品質・使い勝手ともに満足しており、同様のニーズをお持ちの方にぜひご検討いただきたい一品です。",
        "全体的な完成度は高く、「{name}」を選んで正解だったと感じています。多少の改善余地はあるものの、それを補って余りある満足感がございます。ご購入を迷われている方の参考になれば幸いです。",
        "「{name}」は期待に応える、信頼性の高い商品でした。長期にわたって使い続けられる品質だと確信しており、自信を持ってお勧めいたします。",
    ],
    star_ratings=["★★★★★ (5/5)", "★★★★☆ (4/5)", "★★★★½ (4.5/5)"],
    usage_periods=["約1ヶ月", "約2ヶ月", "半年ほど", "1週間ほど", "2週間ほど"],
)


# ──────────────────────────────────────
# スタイル② カジュアルレビュー
# ──────────────────────────────────────
STYLE_CASUAL = StyleTemplate(
    name="カジュアルレビュー",
    title_templates=[
        "{name}を{period}使った感想、正直に言います！（{stars}）",
        "【リアルな話】{name}ってどうなの？買って{period}でわかったこと",
        "{name}、買って後悔した？正直レポ！評価は{stars}",
        "みんなが気になってる{name}を実際に試してみた話【{stars}】",
    ],
    intro_backgrounds=[
        "ずっと気になってて、ついに買っちゃいました！",
        "SNSで見かけて「これ欲しい！」ってなって即ポチしました。",
        "友達が使ってて良さそうだったので、自分も試してみることに。",
        "レビューを読みまくって悩んだ末に、えいっと購入しました！",
    ],
    first_impressions=[
        "届いたときの感想は「おっ、思ったよりいいじゃん！」でした。",
        "箱を開けた瞬間、なんか「当たり引いたな」って直感しました。",
        "手に取ったらすぐわかる、これ作りがしっかりしてる！",
        "第一印象はバッチリ。見た目も質感もいい感じです。",
    ],
    good_lead_ins=[
        "で、実際使ってみて一番テンション上がったのが、",
        "これは正直びっくりしたんですけど、",
        "毎日使ってて「これほんとに買ってよかった！」って思うのが、",
        "友達にも自慢したくなるくらい気に入ってるのが、",
    ],
    connectors=[
        "あと、",
        "それと、",
        "さらに、",
        "他にも、",
        "地味にすごいのが、",
        "もうひとつ言うと、",
        "これも大事なポイントで、",
    ],
    endings_positive=[
        "ってのが思った以上で、めちゃくちゃ助かってます。",
        "っていうのがリアルな感想です。これだけで買う価値あり！",
        "って感じで、使うたびに「いい買い物したな〜」ってなります。",
        "ってのはデカい。毎日使うものだからこそ大事ですよね。",
        "というのが予想外によくて、普通にテンション上がりました。",
    ],
    concern_leads=[
        "ただ、正直に言うと気になるとこもあって、",
        "ちょっとだけ欲を言うと、",
        "完璧か？って言われると、うーん、",
        "強いて言うなら惜しいなって思ったのが、",
    ],
    concern_endings=[
        "ってとこは、もうちょい頑張ってほしかったかな。",
        "って部分は、次のバージョンで改善されたら嬉しいです。",
        "ってのは地味に不便でした。慣れれば気にならないけどね。",
    ],
    outro_templates=[
        "トータルで言うと、「{name}」はぜんぜんアリだと思います！多少気になるとこはあっても、それを超える満足感があるので、迷ってる人はとりあえず試してみてほしいです。",
        "結論：買って正解でした！「{name}」は使えば使うほど好きになってく系の商品です。ぜひ参考にしてみてください！",
        "というわけで、「{name}」の購入は全然おすすめできます。コスパも含めて、かなり満足度高めです。気になってる人の背中を押せたら嬉しいです！",
    ],
    star_ratings=["★5（最高！）", "★4（かなりいい）", "★4.5（ほぼ満点）"],
    usage_periods=["1週間", "2週間", "1ヶ月", "2ヶ月", "半年近く"],
)


# ──────────────────────────────────────
# スタイル③ SNS用（短め・インパクト重視）
# ──────────────────────────────────────
STYLE_SNS = StyleTemplate(
    name="SNS用",
    title_templates=[
        "{name}が想像以上だった話 {stars}",
        "{name}レビュー 実際に{period}使ってみた正直な感想",
        "{name}買ってみた！{stars}の理由を語ります",
        "【{name}】これ買いです。{stars}",
    ],
    intro_backgrounds=[
        "ずっと気になってたやつ、ついに買いました。",
        "SNSで見かけて即ポチしたやつのレポです！",
        "友達に勧められて試してみたら想像以上でした。",
        "セールで見つけて運命を感じて即決した一品。",
    ],
    first_impressions=[
        "届いた瞬間「あ、これいいやつだ」ってなりました。",
        "開封してすぐわかる、クオリティ高い！",
        "想像よりずっと良くてテンション上がりました。",
        "第一印象から好き。見た目も質感も合格点以上。",
    ],
    good_lead_ins=[
        "特によかったのが、",
        "一番感動したのが、",
        "これは推せると思ったのが、",
        "毎日使ってて嬉しいのが、",
    ],
    connectors=[
        "あと",
        "さらに",
        "それと",
        "他にも",
        "地味にすごいのが",
        "もう一個言うと",
    ],
    endings_positive=[
        "→ これほんとに助かる",
        "→ もっと早く買えばよかった",
        "→ これは推せる",
        "→ 毎日のストレスがひとつ減った感じ",
        "→ 地味だけど一番大事なとこだと思う",
    ],
    concern_leads=[
        "強いて言うと惜しいのが、",
        "ひとつだけ欲を言うなら、",
        "改善してほしいのが、",
    ],
    concern_endings=[
        "→ ここだけ次に期待",
        "→ 慣れれば気にならないかも",
        "→ 小さい不満だけど一応シェア",
    ],
    outro_templates=[
        "総合的には大満足です。「{name}」、迷ってる人はぜひ試してみて。後悔しないと思います！",
        "結論：買い。「{name}」はコスパ含めて本当におすすめできます。参考になれば！",
        "「{name}」は正直かなり良かったです。また買うかと言われたら即答でYES。",
    ],
    star_ratings=["★5 / 5", "★4 / 5", "★4.5 / 5"],
    usage_periods=["1週間", "2週間", "1ヶ月", "約2ヶ月"],
)

# スタイル一覧（番号 → スタイル）
STYLES = {
    "1": STYLE_FORMAL,
    "2": STYLE_CASUAL,
    "3": STYLE_SNS,
}


# ============================================================
# レビュー生成コア
# ============================================================

NEGATIVE_KEYWORDS = [
    "惜しい", "残念", "気になる", "難点", "欠点", "デメリット",
    "重い", "高い", "遅い", "弱い", "短い", "使いにくい", "わかりにくい",
    "イマイチ", "いまいち", "もう少し", "改善", "不満",
]

def split_points(points: list) -> tuple:
    """ポイントをネガティブキーワードで良い点 / 気になる点に振り分ける"""
    good, concern = [], []
    for p in points:
        if any(kw in p for kw in NEGATIVE_KEYWORDS):
            concern.append(p)
        else:
            good.append(p)
    if len(concern) > len(points) // 2:
        concern = concern[:max(1, len(points) // 4)]
        good = [p for p in points if p not in concern]
    return good, concern


def build_body(name: str, good: list, concern: list, s: StyleTemplate) -> str:
    """スタイルに従って段落構成の本文を組み立てる"""
    paragraphs = []

    # 段落① 購入背景 + 第一印象
    paragraphs.append(pick(s.intro_backgrounds) + pick(s.first_impressions))

    # 段落② 良かった点
    if good:
        sentences = []
        last_conn = ""
        for i, pt in enumerate(good):
            p = clean(pt)
            ending = pick(s.endings_positive)
            if i == 0:
                sentences.append(f"{pick(s.good_lead_ins)}{p}{ending}")
            else:
                conn = pick_no_repeat(s.connectors, last_conn)
                last_conn = conn
                sentences.append(f"{conn}{p}{ending}")
        paragraphs.append("\n".join(sentences))

    # 段落③ 気になる点（あれば）
    if concern:
        lines = []
        lead = pick(s.concern_leads)
        for i, pt in enumerate(concern):
            p = clean(pt)
            ending = pick(s.concern_endings)
            if i == 0:
                lines.append(f"{lead}{p}{ending}")
            else:
                lines.append(f"{s.connectors[0]}{p}{ending}")
        paragraphs.append("\n".join(lines))

    # 段落④ まとめ
    paragraphs.append(pick(s.outro_templates).format(name=name))

    return "\n\n".join(paragraphs)


def generate_review(name: str, points: list, style: StyleTemplate) -> dict:
    """レビューデータを生成して辞書で返す"""
    stars = pick(style.star_ratings)
    period = pick(style.usage_periods)
    title = pick(style.title_templates).format(name=name, stars=stars, period=period)
    good, concern = split_points(points)
    body = build_body(name, good, concern, style)
    return {"title": title, "stars": stars, "period": period, "body": body, "style": style.name}


# ============================================================
# 出力フォーマッター
# ============================================================

def format_amazon(name: str, result: dict) -> str:
    """Amazon風フォーマット"""
    lines = []
    lines.append(f"{'=' * 60}")
    lines.append(f"  商品名  : {name}")
    lines.append(f"  総合評価: {result['stars']}")
    lines.append(f"  使用期間: {result['period']}")
    lines.append(f"{'─' * 60}")
    lines.append(f"  {result['title']}")
    lines.append(f"{'─' * 60}")
    lines.append("")

    # 本文をそのまま表示（段落ごとにインデント）
    for para in result["body"].split("\n\n"):
        for line in para.split("\n"):
            lines.append(f"  {line}")
        lines.append("")

    lines.append(f"{'─' * 60}")
    lines.append(f"  参考になった？  👍 役に立った  💬 コメントする")
    lines.append(f"{'=' * 60}")
    return "\n".join(lines)


def format_rakuten(name: str, result: dict) -> str:
    """楽天風フォーマット（見出し区切り付き）"""
    lines = []
    lines.append(f"★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★")
    lines.append(f"  {result['title']}")
    lines.append(f"★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★")
    lines.append(f"")
    lines.append(f"  【商 品】{name}")
    lines.append(f"  【評 価】{result['stars']}")
    lines.append(f"  【期 間】{result['period']}")
    lines.append(f"")

    paras = result["body"].split("\n\n")
    headings = ["◆ 購入のきっかけ", "◆ 良かった点", "◆ 気になった点", "◆ 総 評"]

    for i, para in enumerate(paras):
        heading = headings[i] if i < len(headings) else f"◆ ポイント {i+1}"
        lines.append(f"  {heading}")
        lines.append(f"  {'─' * 40}")
        for line in para.split("\n"):
            lines.append(f"  {line}")
        lines.append("")

    lines.append(f"★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★")
    lines.append(f"  購入者レビュー｜{datetime.now().strftime('%Y年%m月%d日')}")
    lines.append(f"★━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━★")
    return "\n".join(lines)


def format_blog(name: str, result: dict) -> str:
    """ブログ風フォーマット（Markdown スタイル）"""
    lines = []
    lines.append(f"# {result['title']}")
    lines.append(f"")
    lines.append(f"> 評価：{result['stars']}　|　使用期間：{result['period']}　|　{datetime.now().strftime('%Y/%m/%d')}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")

    paras = result["body"].split("\n\n")
    headings = [
        "## はじめに",
        "## 実際に使ってみて",
        "## 気になった点",
        "## まとめ・総評",
    ]

    for i, para in enumerate(paras):
        heading = headings[i] if i < len(headings) else f"## ポイント {i+1}"
        lines.append(heading)
        lines.append("")
        lines.append(para)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(f"この記事が参考になったら、ぜひシェアをお願いします！")
    return "\n".join(lines)


# フォーマット一覧
FORMATTERS = {
    "1": ("Amazon風",  format_amazon),
    "2": ("楽天風",    format_rakuten),
    "3": ("ブログ風",  format_blog),
}


# ============================================================
# 表示・保存
# ============================================================

def display_result(name: str, result: dict, fmt_key: str):
    formatter_name, formatter_fn = FORMATTERS[fmt_key]
    formatted = formatter_fn(name, result)

    print(f"\n{'=' * 62}")
    print(f"  スタイル：{result['style']}　|　フォーマット：{formatter_name}")
    print(f"{'=' * 62}")
    print()
    print(formatted)


def save_to_file(name: str, result: dict, fmt_key: str):
    formatter_name, formatter_fn = FORMATTERS[fmt_key]
    formatted = formatter_fn(name, result)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    style_tag = result["style"].replace(" ", "_")
    filename = f"review_{style_tag}_{formatter_name}_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"スタイル　　: {result['style']}\n")
        f.write(f"フォーマット: {formatter_name}\n")
        f.write(f"商品名　　　: {name}\n")
        f.write(f"生成日時　　: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("\n" + "=" * 50 + "\n\n")
        f.write(formatted + "\n")

    print(f"\n  💾 保存しました: {filename}")


# ============================================================
# 対話メニュー
# ============================================================

def choose_style() -> StyleTemplate:
    print("\n  スタイルを選んでください:")
    print("    1. 丁寧レビュー  （丁寧語・信頼感重視）")
    print("    2. カジュアル    （話し言葉・親しみやすさ重視）")
    print("    3. SNS用         （短め・インパクト重視）")
    while True:
        key = input("  番号を入力 > ").strip()
        if key in STYLES:
            return STYLES[key]
        print("  ⚠️  1〜3 の番号を入力してください。")


def choose_format() -> str:
    print("\n  出力フォーマットを選んでください:")
    print("    1. Amazon風  （評価・使用期間・本文の定番構成）")
    print("    2. 楽天風    （見出しブロックで段落を明示）")
    print("    3. ブログ風  （Markdown見出し付き・記事スタイル）")
    while True:
        key = input("  番号を入力 > ").strip()
        if key in FORMATTERS:
            return key
        print("  ⚠️  1〜3 の番号を入力してください。")


def input_product_name() -> str:
    print("\n  商品名を入力してください:")
    while True:
        name = input("  商品名 > ").strip()
        if name:
            return name
        print("  ⚠️  商品名を入力してください。")


def input_review_points() -> list:
    print("\n  レビューのポイントを1行ずつ入力してください。")
    print("  ヒント：「惜しい」「重い」「高い」等のネガティブワードを含むと")
    print("          「気になる点」段落として自動分類されます。")
    print("  （終わったら空のままEnterを押してください）\n")
    points, index = [], 1
    while True:
        pt = input(f"  ポイント {index} > ").strip()
        if pt == "":
            if not points:
                print("  ⚠️  最低1つはポイントを入力してください。")
                continue
            break
        points.append(pt)
        index += 1
    return points


# ============================================================
# メイン
# ============================================================

def main():
    print("=" * 62)
    print("  🛍️  レビュー生成ツール v3")
    print("=" * 62)

    # ① 商品名
    name = input_product_name()

    # ② ポイント入力
    points = input_review_points()

    # ③ スタイル選択
    style = choose_style()

    # ④ フォーマット選択
    fmt_key = choose_format()

    # ⑤ 生成・表示
    print("\n  ⏳ レビューを生成中...")
    result = generate_review(name, points, style)
    display_result(name, result, fmt_key)

    # ⑥ 保存
    ans = input("\nファイルに保存しますか？ (y / n) > ").strip().lower()
    if ans == "y":
        save_to_file(name, result, fmt_key)

    # ⑦ 再生成ループ（スタイル/フォーマット変更も可能）
    while True:
        print("\n再生成しますか？")
        print("  1. 同じスタイル・フォーマットで再生成")
        print("  2. スタイルとフォーマットを変えて再生成")
        print("  3. 終了")
        choice = input("  番号を入力 > ").strip()

        if choice == "1":
            print("\n  ⏳ 再生成中...")
            result = generate_review(name, points, style)
            display_result(name, result, fmt_key)

        elif choice == "2":
            style = choose_style()
            fmt_key = choose_format()
            print("\n  ⏳ 再生成中...")
            result = generate_review(name, points, style)
            display_result(name, result, fmt_key)

        else:
            break

        ans = input("\nこのパターンを保存しますか？ (y / n) > ").strip().lower()
        if ans == "y":
            save_to_file(name, result, fmt_key)

    print("\n  👋 ご利用ありがとうございました！\n")


if __name__ == "__main__":
    main()
