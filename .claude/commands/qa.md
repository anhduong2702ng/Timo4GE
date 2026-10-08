# QA kiểm tra chất lượng

Đọc `output/html/toan-bo-de-cuong.html` và kiểm tra chất lượng toàn bộ 38 bài tập.

## Checklist
1. **Keywords**: mỗi bài có keyword hợp lý không? Gom cụm từ chưa? % có quá cao không (>50% cảnh báo)?
2. **Think-chain**: có bài nào LỘ ĐÁP ÁN trong phần phân tích không? (tuyệt đối cấm)
3. **Diagrams**: 4 bài (TN18, TL8, TL11, TL13) có diagram `.mathdiag` nằm trong `keyword-analysis` không?
4. **Solutions**: tất cả 38 bài có `<details class="solution">` với text "(nhập mật khẩu)" không?
5. **Structure**: mỗi bài có đủ: ex-head, prompt, kw-toolbar, theory-link, keyword-analysis, textarea, solution, status?
6. **Password gate**: JS function `checkSolution` có trong `<script>` block không?

## Output format
In bảng kết quả:
```
| Bài  | KW | %  | Think | Diag | Sol | Status |
|------|----|----|-------|------|-----|--------|
| TN1  | 4  | 50 | OK    | -    | OK  | OK     |
```

Dùng Python script với `python -I` + `sys.stdout.reconfigure(encoding='utf-8')`.
