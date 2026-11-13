#import "@preview/cetz:0.3.2": canvas, draw

#set page(margin: (x: 0.7cm, y: 0.6cm))
#set text(font: "Arial", size: 10pt)
#set par(justify: false, leading: 0.5em)

#text(size: 16pt, weight: "bold")[AI & Tương Lai Ngành Kế Toán]
#h(1fr)
#text(size: 9pt, fill: gray)[Tuần 26 tháng 3, 2026]
#v(0.15em)
#text(size: 10pt)[Buổi trò chuyện giữa Thi (AI Consultant) và Ngân (Kế toán viên) về tác động của AI lên ngành kế toán, đặc biệt là Big Four. Từ use case cụ thể, cách "sell" AI cho công ty, đến tương lai nghề nghiệp và khóa học 4 buổi.]

#v(0.4em)

#block(fill: luma(230), inset: 4pt, width: 100%)[#text(size: 11pt, weight: "bold")[1. Big Four là "Bad Idea" trong kỷ nguyên AI]]

#v(0.3em)

#grid(
  columns: (1fr, 1fr),
  gutter: 1.2em,
  [
    *AI đã phá vỡ lợi thế cốt lõi của Big Four.* Trước 2022, chỉ EY hay KPMG mới đủ tiền đầu tư tool đọc invoice tự động. Bây giờ bất kỳ công ty nhỏ nào cũng làm được.

    #align(center)[
      #canvas(length: 1cm, {
        import draw: *
        let bw = 2.2
        let bh = 0.6
        let g = 0.4
        rect((0, 0), (bw, bh), fill: luma(235), stroke: 0.5pt, radius: 2pt)
        content((bw/2, bh/2), text(size: 6.5pt)[Technology])
        rect((bw + g, 0), (2*bw + g, bh), fill: luma(235), stroke: 0.5pt, radius: 2pt)
        content((1.5*bw + g, bh/2), text(size: 6.5pt)[Data scale])
        rect((2*bw + 2*g, 0), (3*bw + 2*g, bh), fill: luma(235), stroke: 0.5pt, radius: 2pt)
        content((2.5*bw + 2*g, bh/2), text(size: 6.5pt)[Client base])
        line((bw + 0.04, bh/2), (bw + g - 0.04, bh/2), stroke: 0.5pt + red, mark: (end: "stealth", fill: red, scale: 0.4))
        line((2*bw + g + 0.04, bh/2), (2*bw + 2*g - 0.04, bh/2), stroke: 0.5pt + red, mark: (end: "stealth", fill: red, scale: 0.4))
      })
    ]

    Big Four còn giữ được relationship và client base, nhưng *không đủ* khi technology và data đã bị democratize. Công ty nhỏ 5-6 người giờ cạnh tranh được với tập đoàn quốc tế.
  ],
  [
    *3 lợi thế bị phá vỡ:*
    + *Technology độc quyền* — AI mã nguồn mở và giá rẻ khiến tool trước đây hàng triệu đô nay ai cũng có.
    + *Data scale* — AI xử lý data rẻ hơn, nhanh hơn, không cần đội ngũ lớn.
    + *Client base* — còn giữ nhưng đang bị xói mòn bởi dịch vụ cá nhân hóa từ firm nhỏ.

    *Kết quả:* Đội 12–20 người có thể cạnh tranh trực tiếp với tập đoàn quốc tế. Những công ty kế toán nhỏ mà cứ làm manual thì *chắc chắn sẽ biến mất* — đối thủ dùng AI 2–3 năm sau sẽ hất cẳng.
  ]
)

#v(0.4em)

#block(fill: luma(50), inset: 4pt, width: 100%)[#text(size: 11pt, weight: "bold", fill: white)[2. Use case: Từ invoice đến Trial Balance]]

#v(0.3em)

#grid(
  columns: (1fr, 1fr),
  gutter: 1.2em,
  [
    *Invoice tự động — chỉ 1 nút bấm.* Chụp hình invoice, bỏ vào folder, bấm AI → ra Excel với Transaction ID, vendor, description, số tiền, VAT, tổng cộng.

    #align(center)[
      #canvas(length: 1cm, {
        import draw: *
        let bw = 1.3
        let bh = 0.55
        let g = 0.3
        rect((0, 0), (bw, bh), fill: rgb("#e8f5e9"), stroke: 0.5pt, radius: 2pt)
        content((bw/2, bh/2), text(size: 7pt)[Chụp])
        rect((bw + g, 0), (2*bw + g, bh), fill: rgb("#e8f5e9"), stroke: 0.5pt, radius: 2pt)
        content((1.5*bw + g, bh/2), text(size: 7pt)[Folder])
        rect((2*bw + 2*g, 0), (3*bw + 2*g, bh), fill: rgb("#c8e6c9"), stroke: 0.5pt, radius: 2pt)
        content((2.5*bw + 2*g, bh/2), text(size: 7pt)[AI])
        rect((3*bw + 3*g, 0), (4*bw + 3*g, bh), fill: rgb("#a5d6a7"), stroke: 0.5pt, radius: 2pt)
        content((3.5*bw + 3*g, bh/2), text(size: 7pt)[Excel])
        line((bw + 0.04, bh/2), (bw + g - 0.04, bh/2), stroke: 0.5pt, mark: (end: "stealth", fill: black, scale: 0.4))
        line((2*bw + g + 0.04, bh/2), (2*bw + 2*g - 0.04, bh/2), stroke: 0.5pt, mark: (end: "stealth", fill: black, scale: 0.4))
        line((3*bw + 2*g + 0.04, bh/2), (3*bw + 3*g - 0.04, bh/2), stroke: 0.5pt, mark: (end: "stealth", fill: black, scale: 0.4))
      })
    ]

    *So sánh thời gian:* Nhập tay 1 tiếng + check 30 phút = 1.5 tiếng. AI nhập 20 phút + check kỹ 1 tiếng = 1 tiếng 20 phút. Tiết kiệm ~30 phút mỗi batch. Lo ngại "AI sai thì sao?" — nhập tay cũng phải check lại, dù check gấp đôi vẫn nhanh hơn.
  ],
  [
    *Bank Statement → Trial Balance trong 5 phút.* AI phân loại transaction (cash in/out, expense, income), gán account code, tính debit/credit, xuất trial balance. Thậm chí *tự tạo danh sách câu hỏi investigate* (tiền rent ở đâu? one-off hay ongoing?).

    *Điểm đột phá:* AI bây giờ có *self-check loop* — làm xong, kiểm tra, chỉnh sửa, kiểm tra lại cho đến khi balance match. Giống như cách kế toán viên làm, nhưng trong vài phút.

    *Demo thực tế:* Thi ngồi ở nhà hàng khách hàng, khách đưa bank statement (Excel), vừa nói chuyện 5 phút vừa để AI chạy. Xong hỏi ngay: "Sao không thấy tiền rent chị?" — khách ngỡ ngàng.

    AI cũng xử lý được PDF xấu (chụp hình, scan), PNG bank statement — tất cả các định dạng khó.
  ]
)

#v(0.4em)

#block(fill: luma(230), inset: 4pt, width: 100%)[#text(size: 11pt, weight: "bold")[3. Payslip cá nhân hóa & Statutory Filing]]

#v(0.3em)

#grid(
  columns: (1fr, 1fr),
  gutter: 1.2em,
  [
    *Payslip: từ "không giải thích được" đến tư vấn từng case.*

    #align(center)[
      #canvas(length: 1cm, {
        import draw: *
        rect((0, 0), (2.2, 0.8), fill: rgb("#ffcdd2"), stroke: 0.5pt + rgb("#e53935"), radius: 2pt)
        content((1.1, 0.4), text(size: 6.5pt, weight: "bold")[Manual: chung chung])
        rect((2.8, 0), (5.0, 0.8), fill: rgb("#c8e6c9"), stroke: 0.5pt + rgb("#43a047"), radius: 2pt)
        content((3.9, 0.4), text(size: 6.5pt, weight: "bold")[AI: từng case cụ thể])
        line((2.24, 0.4), (2.76, 0.4), stroke: 0.5pt, mark: (end: "stealth", fill: black, scale: 0.4))
      })
    ]

    Ví dụ: đợt tax code change, khách hỏi rất nhiều. Với AI, mỗi payslip kèm giải thích chi tiết theo từng case — khách chưa kịp hỏi thì mình đã gửi giải thích rồi. *Công ty manual làm sao cạnh tranh?*
  ],
  [
    *Statutory Filing:* Nói với AI "Tao đang làm Statutory Filing. Mày làm." → AI xuất file Excel đúng format để import vào phần mềm kế toán (MGM, v.v.).

    *"Luật chơi" riêng cho mỗi người:* AI giống sinh viên tốt nghiệp hạng nhất — rất thông minh, nhưng về công ty mình thì phải theo luật công ty mình. Mình set rule, AI tuân theo. AI của Ngân khác AI của Thi, mỗi người có "luật chơi" hoàn toàn riêng.

    Không cần Prompt Engineering. Chỉ nói chuyện bình thường. Claude Code chỉ là phần mềm — *không có gì phải sợ hết.*
  ]
)

#v(0.4em)

#block(fill: luma(50), inset: 4pt, width: 100%)[#text(size: 11pt, weight: "bold", fill: white)[4. Sell AI vào công ty — kinh nghiệm thực chiến]]

#v(0.3em)

#grid(
  columns: (1fr, 1fr),
  gutter: 1.2em,
  [
    *Resistance theo loại công ty:*
    - *Công ty lớn:* Resistance cao — phải theo hệ thống, khó thuyết phục.
    - *Công ty vừa:* Resistance trung bình — cần demo + số liệu.
    - *Practice nhỏ:* Resistance thấp — "Làm thử đi, được thì làm."

    Vấn đề này liên quan đến *văn hóa công ty.* Có công ty không bao giờ chấp nhận cái mới. Có công ty chỉ cần thấy demo là cho thử.

    #align(center)[
      #canvas(length: 1cm, {
        import draw: *
        rect((0, 0), (1.5, 2.2), fill: rgb("#ffcdd2"), stroke: 0.5pt, radius: 2pt)
        rect((1.9, 0), (3.4, 1.5), fill: rgb("#fff9c4"), stroke: 0.5pt, radius: 2pt)
        rect((3.8, 0), (5.3, 0.8), fill: rgb("#c8e6c9"), stroke: 0.5pt, radius: 2pt)
        content((0.75, -0.3), text(size: 7pt)[Big Corp])
        content((2.65, -0.3), text(size: 7pt)[Mid-size])
        content((4.55, -0.3), text(size: 7pt)[Practice nhỏ])
        content((2.65, 2.5), text(size: 7pt, fill: gray)[← Mức resistance])
      })
    ]
  ],
  [
    *Quy trình sell (kinh nghiệm Thi):*
    + Học ở nhà, tự làm trước.
    + Tìm 1 use case đơn giản (tiết kiệm vài chục tiếng/tháng).
    + Làm demo, quay video.
    + Trình bày cấp trên với số liệu cụ thể.
    + Nếu được → triển khai thử 1 khách → mở rộng dần.
    + Nếu chưa → giữ kiến thức, đợi cơ hội hoặc đổi công ty.

    *Câu chuyện Thi:* Bắt đầu là intern ở công ty buôn bán đồ cổ. Ngày thứ 2 đã đề xuất cải tiến. Bị xem là "điên," nhưng làm demo quay video gửi lại → được thử → 1 khách → 2 khách → 3 khách → bây giờ khách hàng nghe theo và mua phần mềm.

    *Hai lời khuyên cho Ngân:*
    + *Học cho mình trước* — phòng khi công ty bị disrupt, mình còn qua chỗ khác làm.
    + *Thử sell solution cho chính công ty mình* — không dễ, nhưng làm được thì lên cấp độ khác.
  ]
)

#v(0.4em)

#block(fill: luma(230), inset: 4pt, width: 100%)[#text(size: 11pt, weight: "bold")[5. 4 Cấp độ sử dụng AI & Tương lai]]

#v(0.3em)

#grid(
  columns: (1fr, 1fr),
  gutter: 1.2em,
  [
    *4 Level sử dụng AI:*

    #align(center)[
      #canvas(length: 0.8cm, {
        import draw: *
        rect((0, 0), (1.4, 0.9), fill: rgb("#e3f2fd"), stroke: 0.5pt, radius: 2pt)
        rect((1.8, 0), (3.2, 1.5), fill: rgb("#bbdefb"), stroke: 0.5pt, radius: 2pt)
        rect((3.6, 0), (5.0, 2.1), fill: rgb("#64b5f6"), stroke: 0.5pt, radius: 2pt)
        rect((5.4, 0), (6.8, 2.8), fill: rgb("#1565c0"), stroke: 0.5pt, radius: 2pt)
        content((0.7, 0.45), text(size: 6pt)[L1])
        content((2.5, 0.75), text(size: 6pt)[L2])
        content((4.3, 1.05), text(size: 6pt, fill: white)[L3])
        content((6.1, 1.4), text(size: 6pt, fill: white)[L4])
        content((0.7, -0.3), text(size: 5.5pt)[1+1])
        content((2.5, -0.3), text(size: 5.5pt)[1+n AI])
        content((4.3, -0.3), text(size: 5.5pt)[5×1 AI])
        content((6.1, -0.3), text(size: 5.5pt)[5×5 AI])
      })
    ]

    - *Level 1:* 1 người + 1 AI
    - *Level 2:* 1 người + nhiều AI
    - *Level 3:* 1 người quản 5 người thật, mỗi người dùng 1 AI
    - *Level 4:* 1 người quản 5 người thật, mỗi người dùng 5 AI

    *Kết quả:* Team 5–6 người làm được công việc của công ty 50 người ngày xưa.
  ],
  [
    *Khóa học 4 buổi (taster):*
    + *Nguyên lý AI* — ecosystem Python + Claude Code + Tools.
    + *Thực hành* — demo Trial Balance, invoice, bank statement.
    + *Ứng dụng* — identify problem, quản lý AI agents, sell solution.
    + *Tương lai & Mindset* — đọc báo không hoang mang, kế hoạch cá nhân.

    Triết lý: *học nguyên lý, không học tool cụ thể.* Giống như học kế toán xong xài Xero hay QuickBooks đều được — 1 tuần là quen. Lớp nhỏ để tâm sự, thảo luận cụ thể: sáng vô làm gì, cái nào tự động hóa được, 5–10 năm nữa mình sẽ ra sao.

    *Daniel Priestley:* _"This is the most incredible time we're living in."_ Mọi người đều có 5 nhân viên AI tốt nghiệp Harvard, tất cả kỹ năng, chỉ 100 USD/tháng, nằm trong túi. Nhưng chưa ai ready — giống intern bất ngờ lên manager với 5 người dưới quyền.

    *Truyền thông:* Social media đăng tiêu cực để kiếm view ("Kế toán mất việc!"). Học AI đúng cách = *đọc báo không còn hoang mang.*
  ]
)
