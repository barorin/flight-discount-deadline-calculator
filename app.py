import datetime

import pandas as pd
import streamlit as st

# アプリのタイトルと説明
st.set_page_config(page_title="航空券割引締切日計算ツール", page_icon="✈️", layout="wide")

st.title("ANA SUPER VALUEとJAL先得割引の締切日計算ツール")
st.markdown("搭乗日と航空会社・割引プランを選択すると、予約締切日がわかります。")
st.markdown("---")

# 航空会社と割引プランの定義
ana_plans = {
    "SUPER VALUE 75": 75,
    "SUPER VALUE 55": 55,
    "SUPER VALUE 45": 45,
    "SUPER VALUE 28": 28,
    "SUPER VALUE 21": 21,
    "VALUE 7": 7,
    "VALUE 3": 3,
    "VALUE 1": 1,
}

jal_plans = {
    "ウルトラ先得": 75,
    "スーパー先得": 55,
    "先得割引タイプB": 45,
    "先得割引タイプA": 28,
    "特便割引21": 21,
    "特便割引7": 7,
    "特便割引3": 3,
    "特便割引1": 1,
}

# 入力フォーム
# 搭乗日の入力
departure_date = st.date_input(
    "搭乗日を選択してください", datetime.date.today() + datetime.timedelta(days=30)
)

# 航空会社の選択
airline = st.radio("航空会社を選択してください", ["ANA", "JAL", "両方"])

# 選択した航空会社に応じて割引プランを表示
selected_plans = []

if airline == "ANA" or airline == "両方":
    ana_selected_plans = st.multiselect(
        "ANAの割引プランを選択してください（複数選択可）",
        list(ana_plans.keys()),
        default=[
            "SUPER VALUE 75",
            "SUPER VALUE 55",
            "SUPER VALUE 45",
            "SUPER VALUE 28",
            "SUPER VALUE 21",
            "VALUE 7",
            "VALUE 3",
            "VALUE 1",
        ],
    )
    # 航空会社名を付けて保存
    for plan in ana_selected_plans:
        selected_plans.append(
            {"航空会社": "ANA", "プラン名": plan, "日数": ana_plans[plan]}
        )

if airline == "JAL" or airline == "両方":
    jal_selected_plans = st.multiselect(
        "JALの割引プランを選択してください（複数選択可）",
        list(jal_plans.keys()),
        default=[
            "ウルトラ先得",
            "スーパー先得",
            "先得割引タイプB",
            "先得割引タイプA",
            "特便割引21",
            "特便割引7",
            "特便割引3",
            "特便割引1",
        ],
    )
    # 航空会社名を付けて保存
    for plan in jal_selected_plans:
        selected_plans.append(
            {"航空会社": "JAL", "プラン名": plan, "日数": jal_plans[plan]}
        )

# 締切日の計算と表示
if selected_plans:
    st.markdown("---")
    st.header("締切日一覧")

    results = []
    today = datetime.date.today()

    for plan in selected_plans:
        days_before = plan["日数"]
        deadline_date = departure_date - datetime.timedelta(days=days_before)
        days_left = (deadline_date - today).days

        results.append(
            {
                "航空会社": plan["航空会社"],
                "割引プラン": plan["プラン名"],
                "予約締切日": deadline_date,
                "予約締切まで": days_left,
            }
        )

    # 締切日順にソート
    df = pd.DataFrame(results)
    df = df.sort_values(by=["予約締切日"], ascending=False)

    # データフレームの表示用にカラム名を調整
    display_df = df.copy()

    # データフレームをスタイリング
    def highlight_row(row):
        if row["予約締切まで"] < 0:
            return ["color: red"] * len(row)
        elif row["予約締切まで"] <= 7:
            return ["color: orange"] * len(row)
        else:
            return [""] * len(row)

    # スタイル適用済みのデータフレームを表示
    st.dataframe(
        display_df.style.apply(highlight_row, axis=1), use_container_width=True
    )

# 注意事項
st.markdown("---")
st.markdown("### 注意事項")
st.markdown(
    """
- 締切日は搭乗日の何日前かで計算されます。
- このツールは締切日の目安を計算するものです。航空会社の公式情報と異なる場合は公式情報を優先してください。
- 各プランの詳細や運賃については各航空会社の公式サイトでご確認ください。
"""
)
