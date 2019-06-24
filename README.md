# LineBot 開発

LINEのMessage APIを使ってBotを作る．

## 構造

1. Botアカウントのトークルームにメッセージを送ると，AWSのEC2インスタンスにイベント情報がHTTPSで送られる．
2. ポート番号443にてnginxがイベント情報を受け取り，socket通信でuWSGIサーバにイベント情報を渡す．
3. 流れてきたイベント情報をPythonのWebフレームワークであるFlaskで処理して返信を生成し，トークルームに送信する．

## 使ったもの

- Hardware
  - AWS EC2
- OS
  - Ubuntu (バージョンは後で追記)
- Web Server
  - Nginx
  - uWSGI

- System Manager

  - systemd

- Language

  - Python

- Framework

  - Flask

  