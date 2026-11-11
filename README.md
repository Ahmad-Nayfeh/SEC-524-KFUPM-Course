# SEC 524 – OT Forensics Coursework

<div dir="rtl">

## ✅ الملفات التي تُسلَّم موجودة كلها في مجلد واحد: [`FINAL_SUBMISSION`](FINAL_SUBMISSION)

| الملف | ماذا تفعل به |
|---|---|
| `1_Report_SEC524_OT_Forensics.docx` | **التقرير.** اكتب الأسماء (المظلّلة بالأصفر)، ثم احفظه PDF وسلّم الـ PDF |
| `1_Report_SEC524_OT_Forensics.pdf` | نسخة PDF جاهزة للاطلاع (الأسماء فيها فارغة) |
| `2_Presentation_SEC524_OT_Forensics.pptx` | **العرض.** اكتب الأسماء في الشريحة 1، ثم سجّل الفيديو (10 دقائق) |
| `2_Speaker_Script_for_Recording.md` | النص الذي يقرؤه فواز أثناء التسجيل (حوالي 9 دقائق) |
| `3_Supporting_Files.zip` | **الملفات الداعمة.** تُرفع كما هي (أدلة، سكربتات، صور) |

## 📖 لفهم المشروع
حمّل ملف [`START_HERE_Project_Explained.html`](START_HERE_Project_Explained.html) وافتحه في المتصفح، واضغط زر **عربي** في الأعلى.

## 🗂️ سياق المشروع كاملاً
ملف [`PROJECT_CONTEXT_Conversation.md`](PROJECT_CONTEXT_Conversation.md) يشرح بالترتيب كل ما حدث في المحادثة، وكل القرارات، وما يجب فهمه قبل أي سؤال من الدكتور.

## ✏️ أماكن الأسماء (كلها مظلّلة بالأصفر)
1. **التقرير، الصفحة الأولى:** اسم الطالبين، والأرقام الجامعية، واسم الدكتور.
2. **التقرير، الملحق B جدول B2:** الخطوات 1–3 اسم فواز، والخطوات 4–5 اسم صديقك.
3. **العرض، الشريحة 1:** اسم الطالبين.

بعد الكتابة احذف اللون الأصفر.

## 📤 خطوات التسليم على Blackboard
1. التقرير بصيغة **PDF** (من Word: File ← Save As ← PDF).
2. **فيديو** العرض المسجّل.
3. ملف **`3_Supporting_Files.zip`**.

## 💬 أمور تُراجَع مع فواز قبل التسليم
1. هل كان محوّل الإنترنت (NAT) مُطفأً أثناء التجربة؟ التقرير لا يذكر هذه النقطة.
2. تأكيد التواريخ في جدول سلسلة الحيازة (الملحق B).
3. **عدم حذف الأجهزة الافتراضية** حتى صدور الدرجات، لأن الدكتور قد يطلب الملفات الأصلية.
4. تأكيد أن جهاز الـ historian لم يُشغَّل، كما هو مكتوب في التقرير.
5. الملحق E فيه سطر للإفصاح عن استخدام الذكاء الاصطناعي، لأن ملف المتطلبات (القسم 9) يطلبه. قرّروا الصياغة حسب سياسة المقرر.

</div>

---

## Folder map

```
FINAL_SUBMISSION/                   ← everything to submit
START_HERE_Project_Explained.html   ← open in a browser to understand the project (EN / AR)
PROJECT_CONTEXT_Conversation.md     ← full context: what was done, the decisions, and what to discuss with Fawaz
SUPPORTING_FILES/                   ← same content as the zip, browsable on GitHub
OLD_Original_Files/                 ← original files received (brief, Fawaz's drafts). Do NOT submit
```

## Key facts (if the instructor asks)

- **Lab:** OT-PLC `10.20.30.10:1502` and OT-CLIENT `10.20.30.20` on the VirtualBox internal network `OTLAB`, run on 26 Oct 2026.
- **The write:** `incident.pcap` frame 14, 16:31:30.220 UTC, bytes `00 01 00 00 00 06 01 06 00 10 00 5A` = function 06, register 16, value 90.
- **Proof:** PLC echo (+6.9 ms) → audit log `WRITE_APPLIED 50→90` (+3.5 ms) → read-back = 90. The baseline capture has 0 writes.
- **Validation:** tshark and our Python decoder give identical results, and all hashes match.
- **Limit:** we can prove a host, not a person (Modbus has no users).
