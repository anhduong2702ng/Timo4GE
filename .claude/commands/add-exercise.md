# Thêm bài tập mới

Thêm exercise mới vào `output/html/toan-bo-de-cuong.html`.

## Cấu trúc một bài tập
```html
<article class="exercise" id="{{ID}}">
  <div class="ex-head">
    <span class="tag">{{TAG}}</span>
    <h3>{{TITLE}}</h3>
    <span class="source">Nguồn: {{SOURCE}}</span>
  </div>
  <div class="prompt">
    <span class="prompt-label">ĐỀ BÀI</span>
    <p>{{PROMPT với <u class="kw">từ khóa</u>}}</p>
  </div>
  <div class="kw-toolbar">
    <label><input type="checkbox" class="kw-toggle" onchange="toggleKw(this)"> Gạch chân từ khóa</label>
    <label class="analyze-toggle"><input type="checkbox" onchange="toggleAnalyze(this)"> Phân tích từ khóa</label>
  </div>
  <details class="theory-link">
    <summary>Ôn lý thuyết trước</summary>
    <a href="ly-thuyet-day-du.html#{{ANCHOR}}">{{THEORY_TITLE}}</a>
    <p class="theory-remind">{{THEORY_HINT}}</p>
  </details>
  <details class="keyword-analysis">
    <summary>Cùng con phân tích đề</summary>
    <div class="think-chain">
      <div class="think-step"><span class="think-kw">{{KW}}</span><p>{{HINT — chỉ gợi ý, KHÔNG cho đáp án}}</p></div>
      ...
      <div class="think-ask"><b>Đề hỏi gì?</b> {{question}}</div>
      <div class="think-need"><b>Con cần gì?</b> {{steps}}</div>
    </div>
    <!-- Nếu cần diagram: thêm <div class="mathdiag">...</div> ở đây -->
  </details>
  <div class="work-label">BÀI LÀM CỦA CON</div>
  <textarea aria-label="Bài làm {{ID}}" data-save="work-{{ID}}" placeholder="Con làm vào vở hoặc ghi lời giải ở đây…"></textarea>
  <div class="write-lines print-only"></div>
  <details class="solution">
    <summary>Xem lời giải (nhập mật khẩu)</summary>
    <div class="solution-flow">
      {{SOLUTION STEPS}}
      <p class="answer-line"><strong>Đáp số:</strong> {{ANSWER}}</p>
    </div>
  </details>
  <div class="status">Kết quả: <select aria-label="Kết quả {{ID}}" data-save="status-{{ID}}">
    <option>Chưa làm</option><option>Tự làm đúng</option><option>Cần gợi ý</option><option>Sai — cần làm lại</option>
  </select></div>
</article>
```

## Quy tắc
- ID format: TN (trắc nghiệm), TL (tự luận), TT (thử thách) + số
- Think-chain: chỉ GỢI Ý, tuyệt đối KHÔNG cho đáp án
- Keywords: gom cụm từ, target ≤40%
- Nếu bài có sơ đồ đoạn thẳng → dùng `.mathdiag` CSS, đặt trong `keyword-analysis`
- Solution summary phải có text "(nhập mật khẩu)"
