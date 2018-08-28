from flickrapi import FlickrAPI
from urllib.request import urlretrieve
from pprint import pprint
import os, time, sys
import os.path

# API キーの情報

key = "54dd7f9cc449a30be6a29cfb438c6574"
secret = "f6c5abf555890eea"

# 重要：リクエストを送るタイミングが短すぎると画像取得先のサーバを逼迫してしまうか、
# スパムとみなされてしまう可能性があるので、待ち時間を 1 秒間設ける。
wait_time = 1

# コマンドライン引数の 1 番目の値を取得
vehiclename = input('検索項目>>')#本来はsys.argv[1]でコマンドラインから引数を取得
# 画像を保存するディレクトリを作成
if os.path.isdir(vehiclename) == False:
    os.mkdir(vehiclename)
else:
    pass
# 画像を保存するディレクトリを指定
savedir = "./" + vehiclename

# FlickrAPI にアクセス

# FlickrAPI(キー、シークレット、データフォーマット{json で受け取る})
flickr = FlickrAPI(key, secret, format='parsed-json')
result = flickr.photos.search(
    # 検索キーワード
    text = vehiclename,
    # 取得するデータ件数
    per_page = 50,
    # 検索するデータの種類(ここでは、写真)
    media = 'photos',
    # データの並び順(関連順)
    sort = 'relevance',
    # UI コンテンツを表示しない
    safe_search = 1,
    # 取得したいオプションの値(url_q->画像のアドレスが入っている情報、licence -> ライセンス情報)
    extras = 'url_q, licence'
)

# 結果を表示
photos = result['photos']
if photos == 'non_bmp_map':
    non_bmp_map = { ord('\U0001F44D'): ord('\U0000FFFD')}
    pprint(photos.translate(non_bmp_map))
else:
    pprint(photos)

    # 追記
    for photo in photos['photo']:
        url_q = photo['url_q']
        filepath = savedir + '/' + photo['id'] + '.jpg'
        # ファイルが重複していたらスキップする
        if os.path.exists(filepath): continue
        # データをダウンロードする
        urlretrieve(url_q, filepath)
        # 重要：サーバを逼迫しないように 1 秒待つ
        time.sleep(wait_time)
