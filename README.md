# GoldenDickOnlineTranslate
适用于GoldenDick的在线翻译脚本。

### 使用须知：
1. 轻度使用可选 baidu_fanyi.py ，百度翻译API每月有200万字节的免费额度。重度使用可选 youdao_fanyi.py（免费）或购买百度翻译API服务。
2. 因使用的是百度在线翻译API接口，因此在正式使用前，一定要修改 baidu_fanyi.py 的 appid、secretKey 这两个参数。
3. 百度翻译API账号可以在 http://api.fanyi.baidu.com/api/trans/product/index 注册，并在“开发者信息”中查看到。
4. youdao_fanyi.py 绝大部分代码来自 meow（ http://code.taobao.org/p/youdao_translate/src/ ），仅仅修复了其中的Bug。
