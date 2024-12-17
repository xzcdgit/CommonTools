import fitz  # PyMuPDF

def pdf_to_images(pdf_path, img_path, zoom_x=4.0, zoom_y=4.0, rotation_angle=0):
    # 打开 PDF 文件
    pdf_document = fitz.open(pdf_path)
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        # 设置缩放
        matrix = fitz.Matrix(zoom_x, zoom_y)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        # 处理旋转
        if rotation_angle != 0:
            pix = pix.get_rotated(rotation_angle)
        # 保存图片
        pix.save(f"{img_path}/page_{page_num + 1}.png")

# 示例调用
pdf_to_images("example.pdf", "output_images")
