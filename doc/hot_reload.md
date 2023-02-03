**English is bellow of Japanese**
# ラズパイピコのHot Reload
## できること
- ラズパイピコのビルド/Flash書き込みの自動化
- 監視ファイルの更新、ラズパイピコドライブの追加の両方を監視
- 両条件が揃ったら監視対象ファイルをラズパイピコドライブに書き込む。

## スクリプト動作概要
Windows上で動くことを前提とする。
### tools\python\win\copy_uf2_from_wsl2_to_rzpp.py
- 下記を無限に繰り返す
    1. 指定ファイルの監視
        -  tools\python\win\copy_src_config.py で指定されたファイルの更新日時が更新されたかを監視
        - 更新されたファイルがあれば
            - 焼きこみ待ちキューにファイル情報を追加
    1. ドライブの変化を監視
        - 追加されたドライブがあったら
          - そのドライブに、'/INDEX.HTM','/INFO_UF2.TXT'の両方があるかをチェック
          - 両ファイルが存在していたら
              - 「ラズパイドライブあり」とし、ラズパイドライブレターを保存。
        -  削除されたドライブがあり、ラズパイドライブなら
            - 焼きこみファイルに対応した実行チェック関数を呼び出す。
            - ラズパイドライブレターを無効値に設定。
    1. 更新されたファイルの焼きこみ
        - 「ラズパイドライブあり」かつ「焼きこみ待ちファイルあり」なら
            - 焼きこみ待ちキューからファイル情報を取り出し
            - 焼きこみ対象ファイルをラズパイドライブにコピー
    1. 少し待つ
        - 1秒sleep

### tools\python\win\copy_src_config.py
`src_base_path`
  - 監視対象ファイルの共通部分を指定する。

`src_files`
  - 'file','func'を要素として持つ辞書型変数の配列
  - 各配列要素の`file`要素の前に`src_base_path`を連接した文字列が監視対象ファイルとなる。
    - `r'\\wsl.localhost\Ubuntu-22.04'`とすることでwsl2のファイルを直接指定することができる。
    - Windows側のファイルも指定できる。
  - 当該ファイルが焼きこまれた後、'func'で指定された関数が実行される。
    - 動作確認スクリプトを想定している。

## Tips
- 動作プログラムの最後で`reset_usb_boot(0,0);`を呼び出すことでボタンを押しながらの電源Onと同じ状態に遷移させることができる。
  - `#include "pico/bootrom.h"`が必要
  - リンク対象ライブラリに`pico_bootrom`が必要


# Hot Reload
## What is this do.
- Copy .uf2 fiel to Raspberry pi pico triggerd by detectting both new uf2 is updated and Raspberrypi pico drive is attached to PC.

## Abstruct of script sequence.
This script assumes running on Windows.
### tools\python\win\copy_uf2_from_wsl2_to_rzpp.py
- Run infinit as follows
    1. Watching specified files.
        - Watch the files are updated specified by tools\python\win\copy_src_config.py
        - If find updated file
            - Push the file name to Queue for waiting flashing.
    1. Watching drives.
        - If a drive is attached.
            - Check existing both '/INDEX.HTM' and '/INFO_UF2.TXT' files.
            - If exist both.
                - Change status to "Exist Raspberry pi pico drive" and store the drive letter.
        - If "Raspberry pi pico drive" is detached.
            - Call the function specified with flashed file.
            - Change status to "Raspberry pi pico drive is invalid"
    1. Flash the .uf2 file.
        - if status to "Exist Raspberry pi pico drive" and Queue for waiting flashing is not empty.
            - Copy specified file to Raspberry pi pico drive
    1. Wait
        - sleep 1sec.

### tools\python\win\copy_src_config.py
`src_base_path`
  - Common file path string for all files in `src_files`

`src_files`
  - list of dict, that has menber 'file' and 'func'.
  - Update watching file is specified with string concatinate `src_base_path` and `file` member.
    - You can specify wsl2 files like, `r'\\wsl.localhost\Ubuntu-22.04'`
  - The function specified by 'func' is executed after writing to Raspberry pi pico.
    - This function is assumed as validation script.

## Tips
- If you call `reset_usb_boot(0,0);` just before end of program, that makes Raspberry pi pico to Mass Strage USB mode.
  - `#include "pico/bootrom.h"` is needed.
  - `pico_bootrom`must be linked to the application program.


