# Devcontainer@wsl2 でのRZPPデバッグ
## よく使う手順まとめ
### Windows
```
C:\> cd xx
C:\xx\> venv\Scripts\activate
(venv) C:\xx\> pyocd list
(venv) C:\xx\> pyocd server --allow-remote
```
### wsl2
```
~$ cd pyocd/
~/pyocd$ source venv/bin/activate
(venv) ~/pyocd$ pyocd gdbserver -t rp2040 -uremote:`gawk '/nameserver/{print $2}' /etc/resolv.conf`
```

### Devcontainer
```
target remote host.docker.internal:3333
```

## 環境
### Windows
- VSCodeがインストールされている。
- pythonがインストールされている。
- pythonでvenvを動かせる。(python3 -m venv venv)
- picoprobeが焼かれているRZPPとUSBで接続されている。
- picoprobeが焼かれているRZPPにSWDで接続されているデバッグターゲットに電源が入っている。
### wsl2
- Dockerがインストールされている
- WindowsのVSCodeからwslで接続できる。
- VSCodeに'Dev Containers'拡張がインストールされている
- python3 でvenvを動かせる。(python3 -m venv venv)
### Devcontainer
- RZPP開発環境がインストールされている
- RZPPのビルドができ、.elfがある。

## 環境準備(1回やればよい系)
### Windows
- 適当なディレクトリにpyocd-server実行用のディレクトリを作成する
- そのディレクトリでpython仮想環境を作る
  - `python -m venv venv`
- python仮想環境に入る
  - `venv\Scripts\activate`
- python仮想でpyocdをインストールする。
  - `pip install pyocd`
### wsl2
- 適当なディレクトリにpyocd-server実行用のディレクトリを作成する
- そのディレクトリでpython仮想環境を作る
  - `python3 -m venv venv`
- python仮想環境に入る
  - `source venv/bin/activate`
- python仮想でpyocdをインストールする。
  - `pip install pyocd`
### Devcontainer
- RZPP開発環境がインストールされている
- arm-none-eabi-gdb あるいは gdb-multiarch がインストールされている。
- RZPPのビルドができ、.elfがある。

## 環境準備(PC起動後毎回必要系)
### Windows
- pyocd-server実行用のディレクトリにcdしておく
- python仮想環境に入る
  - `venv\Scripts\activate`
- プローブの接続を確認する
  - `pyocd list`でデバッグアダプタがつながっていることを確認する。
    - 接続されているときの例
      ```
      (.venv) C:\>pyocd list
      #   Probe/Board                        Unique ID          Target
      --------------------------------------------------------------------
      0   Raspberry Pi Picoprobe CMSIS-DAP   E6614864D3979637   n/a
      ```
    - 接続されていないときの例
      ```
      (.venv) C:\>pyocd list
      No available debug probes are connected
      ```
- pyocd プローブサーバーを起動する。
  - `pyocd server --allow-remote`で起動する。
    - 起動時は未接続、起動後接続したときの例
    ```
    (.venv) C:\>pyocd server --allow-remote
    Waiting for a debug probe to be connected...
    0032969 I Serving debug probe Raspberry Pi Picoprobe CMSIS-DAP (E6614864D3979637) on port 5555 [tcp_probe_server]    
    ```
### wsl2
- 事前にWindows側でpyocd プローブサーバーを起動させておく
- gdb-server実行用のディレクトリにcdしておく
- python仮想環境に入る
  - `source venv/bin/activate`
- gdb-serverを起動する。
  - デバッグターゲットまで接続できた時の例
    ```
    (venv) ~/pyocd$ pyocd gdbserver -t rp2040 -uremote:`gawk '/nameserver/{print $2}' /etc/resolv.conf`
    0000796 I Target type is rp2040 [board]
    0006183 I DP IDR = 0x0bc12477 (v2 MINDP rev0) [dap]
    0006281 I AHB-AP#0 IDR = 0x04770031 (AHB-AP var3 rev0) [ap]
    0006403 I AHB-AP#0 Class 0x1 ROM table #0 @ 0xe00ff000 (designer=43b:Arm part=4c0) [rom_table]
    0006434 I [0]<e000e000:SCS v6-M class=14 designer=43b:Arm part=008> [rom_table]
    0006450 I [1]<e0001000:DWT v6-M class=14 designer=43b:Arm part=00a> [rom_table]
    0006466 I [2]<e0002000:BPU v6-M class=14 designer=43b:Arm part=00b> [rom_table]
    0006499 I CPU core #0 is Cortex-M0+ r0p1 [cortex_m]
    0006529 I 2 hardware watchpoints [dwt]
    0006561 I 4 hardware breakpoints, 0 literal comparators [fpb]
    0006609 I Semihost server started on port 4444 (core 0) [server]
    0006676 I GDB server started on port 3333 (core 0) [gdbserver]
    ```
### Devcontainer
- 事前にWindows側でpyocd プローブサーバーを起動させておく
- 事前にwsl2でgdb-serverを起動させておく
- 接続/動作確認
  1. elfファイルを指定してgdbを立ち上げ 
  1. target remoteコマンドでwsl2に接続
     - Docker containerからは`host.docker.internal`でホストアドレスを引ける。
  1. loadコマンドでelfファイルをロード
  1. monitor resetコマンドでターゲットリセット
        ```
        vscode ➜ .../pico/build_rzppw/hello_world/serial (master) $ gdb-multiarch hello_serial.elf
        GNU gdb (Ubuntu 12.1-0ubuntu1~22.04) 12.1
        ：
        Reading symbols from hello_serial.elf...
        (gdb) target remote host.docker.internal:3333
        Remote debugging using host.docker.internal:3333
        0x10004a60 in ?? ()
        (gdb) load
        Loading section .boot2, size 0x100 lma 0x10000000
        Loading section .text, size 0x3cc8 lma 0x10000100
        Loading section .rodata, size 0x1080 lma 0x10003dc8
        Loading section .binary_info, size 0x28 lma 0x10004e48
        Loading section .data, size 0x1c0 lma 0x10004e70
        Start address 0x100001e8, load size 20528
        Transfer rate: 879 bytes/sec, 1466 bytes/write.
        (gdb) monitor reset
        Resetting target  
        ```
  1. ここまでくれば、後は、VS-CodeでCortex-Debugをインストールして、もにょもにょすれば、、、
