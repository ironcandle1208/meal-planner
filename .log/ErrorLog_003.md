# エラーログ - ErrorLog_003.md

## 発生日時
2025/07/22 - 火曜日

## エラー概要
pyproject.tomlファイルのiOS設定セクションで、info_plist_extensionsの構文エラーが発生しました。TOMLフォーマットでは、テーブル内のキーと値の区切りに「:」ではなく「=」を使用する必要があります。

## 原因分析
pyproject.tomlファイルの`[tool.briefcase.app.meals.iOS]`セクション内の`info_plist_extensions`テーブルで、キーと値の区切り文字として「:」（コロン）が使用されていましたが、TOMLフォーマットでは「=」（イコール）を使用する必要があります。

変更前:
```toml
info_plist_extensions = {
    "UILaunchStoryboardName": "LaunchScreen",
    "UIRequiresFullScreen": true,
    ...
}
```

変更後:
```toml
info_plist_extensions = {
    "UILaunchStoryboardName" = "LaunchScreen",
    "UIRequiresFullScreen" = true,
    ...
}
```

この修正は正しいものであり、TOMLフォーマットの仕様に準拠しています。

## 修正箇所
`meals/pyproject.toml`ファイルの`[tool.briefcase.app.meals.iOS]`セクション内の`info_plist_extensions`テーブル

## 修正内容
キーと値の区切り文字を「:」から「=」に変更しました。

```toml
[tool.briefcase.app.meals.iOS.info_plist_extensions]
UILaunchStoryboardName = "LaunchScreen"
UIRequiresFullScreen = true
UISupportedInterfaceOrientations = [
    "UIInterfaceOrientationPortrait",
    "UIInterfaceOrientationLandscapeLeft",
    "UIInterfaceOrientationLandscapeRight",
]
NSCameraUsageDescription = "This app does not use the camera."
NSPhotoLibraryUsageDescription = "This app does not use the photo library."
NSMicrophoneUsageDescription = "This app does not use the microphone."
NSLocationWhenInUseUsageDescription = "This app does not use location services."
```

## 影響範囲
この修正はiOSビルド設定にのみ影響します。アプリケーションのコードや機能には影響しません。ただし、この修正がなければiOSアプリのビルドプロセスが失敗する可能性があります。

## 予防策
1. TOMLファイルを編集する際は、TOMLの構文ルールを確認する
2. 特に異なるフォーマット（JSON、YAML、TOMLなど）間で設定を移行する際は注意が必要
3. 可能であれば、設定ファイルの変更後に構文チェックツールを使用して検証する
4. BriefcaseやBeeWareのドキュメントを参照して、正しい設定形式を確認する