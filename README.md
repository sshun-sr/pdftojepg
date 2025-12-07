# PDF to JPEG Converter

PDFファイルを1ページずつJPEG画像に変換するPythonツールです。

## 機能

- PDFの各ページを個別のJPEG画像に変換
- 解像度（DPI）の指定が可能
- JPEG品質の調整が可能
- コマンドラインから簡単に使用可能

## インストール

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本的な使い方

```bash
python pdf_to_jpeg.py document.pdf
```

これにより、PDFと同じディレクトリに `document_page_001.jpg`, `document_page_002.jpg` などのファイルが生成されます。

### 出力先を指定

```bash
python pdf_to_jpeg.py document.pdf -o output_folder
```

### 解像度と品質を指定

```bash
# 解像度300 DPI、品質90%で変換
python pdf_to_jpeg.py document.pdf -d 300 -q 90
```

## オプション

| オプション | 説明 | デフォルト |
|-----------|------|-----------|
| `-o`, `--output` | 出力先ディレクトリ | PDFと同じディレクトリ |
| `-d`, `--dpi` | 解像度（DPI） | 150 |
| `-q`, `--quality` | JPEG品質（1-100） | 95 |

## 出力ファイル名の形式

変換されたJPEGファイルは以下の形式で保存されます：

```
{元のPDFファイル名}_page_{ページ番号}.jpg
```

例: `document.pdf` → `document_page_001.jpg`, `document_page_002.jpg`, ...

## 必要要件

- Python 3.6以上
- PyMuPDF (fitz)

## ライセンス

MIT