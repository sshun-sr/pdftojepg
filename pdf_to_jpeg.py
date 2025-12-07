#!/usr/bin/env python3
"""
PDF to JPEG Converter
PDFファイルを1ページずつJPEG画像に変換するツール
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF がインストールされていません。")
    print("pip install PyMuPDF を実行してください。")
    sys.exit(1)


def pdf_to_jpeg(pdf_path, output_dir=None, dpi=150, quality=95):
    """
    PDFファイルを1ページずつJPEG画像に変換する

    Args:
        pdf_path (str): 変換するPDFファイルのパス
        output_dir (str): 出力先ディレクトリ（デフォルト: PDFと同じディレクトリ）
        dpi (int): 解像度（デフォルト: 150）
        quality (int): JPEG品質 1-100（デフォルト: 95）

    Returns:
        list: 生成されたJPEGファイルのパスリスト
    """
    # PDFファイルの存在確認
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDFファイルが見つかりません: {pdf_path}")

    # 出力ディレクトリの設定
    if output_dir is None:
        output_dir = os.path.dirname(pdf_path) or "."

    # 出力ディレクトリの作成
    os.makedirs(output_dir, exist_ok=True)

    # PDFファイル名（拡張子なし）を取得
    pdf_basename = Path(pdf_path).stem

    # PDFを開く
    pdf_document = fitz.open(pdf_path)
    total_pages = pdf_document.page_count

    print(f"PDFファイル: {pdf_path}")
    print(f"ページ数: {total_pages}")
    print(f"出力先: {output_dir}")
    print(f"解像度: {dpi} DPI")
    print("-" * 50)

    output_files = []

    # 各ページを処理
    for page_num in range(total_pages):
        page = pdf_document[page_num]

        # 解像度に基づいてズーム率を計算（72 DPI がデフォルト）
        zoom = dpi / 72
        mat = fitz.Matrix(zoom, zoom)

        # ページを画像に変換
        pix = page.get_pixmap(matrix=mat)

        # 出力ファイル名を生成（page_001.jpg形式）
        output_filename = f"{pdf_basename}_page_{page_num + 1:03d}.jpg"
        output_path = os.path.join(output_dir, output_filename)

        # JPEG として保存
        pix.save(output_path, "jpeg", jpg_quality=quality)

        output_files.append(output_path)
        print(f"✓ ページ {page_num + 1}/{total_pages}: {output_filename}")

    # PDFを閉じる
    pdf_document.close()

    print("-" * 50)
    print(f"完了！ {total_pages} ページを変換しました。")

    return output_files


def main():
    parser = argparse.ArgumentParser(
        description="PDFファイルを1ページずつJPEG画像に変換します。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  %(prog)s document.pdf
  %(prog)s document.pdf -o output_folder
  %(prog)s document.pdf -d 300 -q 90
        """
    )

    parser.add_argument(
        "pdf_file",
        help="変換するPDFファイルのパス"
    )

    parser.add_argument(
        "-o", "--output",
        dest="output_dir",
        help="出力先ディレクトリ（デフォルト: PDFと同じディレクトリ）"
    )

    parser.add_argument(
        "-d", "--dpi",
        type=int,
        default=150,
        help="解像度（DPI）（デフォルト: 150）"
    )

    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=95,
        help="JPEG品質 1-100（デフォルト: 95）"
    )

    args = parser.parse_args()

    # 品質の範囲チェック
    if not 1 <= args.quality <= 100:
        print("エラー: JPEG品質は1-100の範囲で指定してください。")
        sys.exit(1)

    try:
        pdf_to_jpeg(
            args.pdf_file,
            output_dir=args.output_dir,
            dpi=args.dpi,
            quality=args.quality
        )
    except Exception as e:
        print(f"エラー: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
