import requests
import urllib.parse

def generate_tts_audio(text, character="sigewinne", emotion=None, output_format="wav", save_temp=True):
    base_url = "http://127.0.0.1:9880/tts"

    params = {
        "character": character,
        "text": text,
        "format": output_format,
        "save_temp": str(save_temp).lower()
    }
    if emotion:
        params["emotion"] = emotion

    encoded_params = urllib.parse.urlencode(params, encoding="utf-8", safe="")
    url = f"{base_url}?{encoded_params}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.content  # 返回音频二进制数据
    except requests.RequestException as e:
        print(f"TTS 请求失败: {e}")
        return None
