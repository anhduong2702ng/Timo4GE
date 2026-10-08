# Patch keywords + diagrams

Chạy patch cập nhật keywords và diagrams cho file `output/html/toan-bo-de-cuong.html`.

## Quy tắc bắt buộc
1. **Phân tích trước** — đọc HTML hiện tại, xác định vấn đề, liệt kê thay đổi trước khi code
2. **Keywords**: gom thành cụm từ có nghĩa, không gạch từng từ lẻ. Target ≤40% text
3. **Diagrams**: dùng CSS `.mathdiag` (Grid + border-radius dashed arcs), KHÔNG dùng SVG. Diagram phải nằm trong `<details class="keyword-analysis">`
4. **Python**: chạy với `python -I`, thêm `sys.stdout.reconfigure(encoding='utf-8')`
5. **QA output**: in ra số keyword và % cho mỗi bài, cảnh báo nếu >50%

## Keyword map format
```python
KW = {
    'TN1': ['cụm từ 1', 'cụm từ 2'],  # gom data+concept
    ...
}
```

## Diagram CSS classes
- `.mathdiag` — CSS Grid container (68px + 1fr)
- `.arc.a` — dashed dome arc above (border-bottom: none)
- `.arc.b` — dashed cup arc below (border-top: none)
- `.mid.u` / `.mid.d` — small difference arcs between bars
- `.bar` — horizontal line with tick marks (::before/::after)
- `.bar .t` — intermediate tick mark
- `.hint` — hint text below diagram

## Sau khi patch
- Mở browser kiểm tra: bấm "Gạch chân từ khóa" → "Phân tích từ khóa" → xem diagram
- Kiểm tra đáp án yêu cầu mật khẩu (000000)
