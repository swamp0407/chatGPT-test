#ライブラリのインポート
import streamlit as st # フロントエンドを扱うstreamlitの機能をインポート
from openai import OpenAI # openAIのchatGPTのAIを活用するための機能をインポート
from dotenv import load_dotenv
import os

load_dotenv(override=True)  # .envを読み込む
API_KEY = os.getenv("OPENAI_API_KEY")
print("読み込まれたAPIキー:", os.getenv("OPENAI_API_KEY"))
# openAIの機能をclientに代入
client = OpenAI()

def join_with_japanese_conjunction(items):
    if not items:
        return ""
    elif len(items) == 1:
        return items[0]
    else:
        return "、".join(items[:-1]) + "、および" + items[-1]

content_kind_of =[
    "会社概要",
    "株価に影響しそうな内容",
    "直近のニュースに関する内容",
    "業界トレンドと競合比較",
    "中期経営計画の要約",
    "M&A・提携の動向",
    "経営課題と今後の注力分野",
    "社長・経営陣の特徴",
    "評判・リスク情報"
]

st.title('訪問する会社の事前調査アプリ')# タイトル

# 訪問先の会社名
company_name_to_gpt = st.sidebar.text_input("訪問先の会社名を入力してください")

# 訪問先の部署名
visit_department_to_gpt = st.sidebar.text_input("訪問先の部署名を入力してください（任意）")
            
# 書かせたい内容のテイストを選択肢として表示する
content_kind_of_to_gpt = st.sidebar.multiselect("重点的にまとめたい内容を選択してください（任意）",options=content_kind_of)

# chatGPTに出力させる文字数
content_maxStr_to_gpt = str(st.sidebar.slider('記事の最大文字数', 100,1000,3000))

selected_topics_text = join_with_japanese_conjunction(content_kind_of_to_gpt)

# chatGPTにリクエストするためのメソッドを設定。引数には書いてほしい内容と文章のテイストと最大文字数を指定
def run_gpt(company_name_to_gpt,topics_to_gpt,content_maxStr_to_gpt,visit_department_to_gpt):
    # リクエスト内容を決める
    request_to_gpt = (
        f"{company_name_to_gpt}という会社に訪問するので、役立つ事前情報をまとめてください。"
        f"内容は{content_maxStr_to_gpt}文字以内で出力してください。"
        + (f"特に、{topics_to_gpt}を分厚めに書いてください。" if topics_to_gpt else "")
        + (f"ちなみに、訪問先の部署名は{visit_department_to_gpt}です。" if visit_department_to_gpt else "")
    )
    
    # 決めた内容を元にclient.chat.completions.createでchatGPTにリクエスト。オプションとしてmodelにAIモデル、messagesに内容を指定
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": request_to_gpt },
        ],
    )

    # 返って来たレスポンスの内容はresponse.choices[0].message.content.strip()に格納されているので、これをoutput_contentに代入
    output_content = response.choices[0].message.content.strip()
    return output_content # 返って来たレスポンスの内容を返す

output_content_text = run_gpt(company_name_to_gpt,content_kind_of_to_gpt,content_maxStr_to_gpt,visit_department_to_gpt)
st.write(output_content_text)