# SEC 524 – OT Forensics Coursework

**Topic:** Operational Technology (OT) forensics. We reconstruct an unauthorised PLC setpoint change (register 16: 50 → 90) from Modbus/TCP packet captures and controller logs, recorded in an isolated VirtualBox lab.

**Status:** the report, the slides and all supporting files are complete. You only need to fill in the names (see step 2 below).

> 🇸🇦 Arabic summary at the bottom of this page. / الملخص بالعربي في آخر الصفحة.

---

## Start here (5 steps)

| # | Do this | Where |
|---|---|---|
| 1 | **Understand the project first.** Download and open the HTML page in any browser. It has diagrams and an **English / عربي** button at the top. | `03_Explainer_Page/SEC524_Project_Explained.html` |
| 2 | **Fill in the names** in the report and in the slides (see the table below). Everything you need to fill in is **highlighted in yellow**. | `01_Final_Report/…FINAL.docx`, `02_Presentation/…FINAL.pptx` |
| 3 | **Export the report to PDF** from Word (File → Save As → PDF). The course requires a PDF. Then check that the contents page numbers are still correct. | `01_Final_Report/` |
| 4 | **Record the 10-minute presentation.** The speaker notes are inside the PowerPoint, and also in a separate script file. The text runs about 9.3 minutes. | `02_Presentation/Speaker_Script.md` |
| 5 | **Upload to Blackboard:** report PDF + recorded video + supporting files (folders `04`, `05`, `06`, zipped). | — |

### What to fill in (highlighted yellow)

| File | Location | What to write |
|---|---|---|
| Report (.docx) | Page 1 (cover) | Student 1 name + ID, Student 2 name + ID, Instructor name |
| Report (.docx) | Appendix B, Table B2 (chain of custody) | Steps 1–3 = the student who ran the lab (Fawaz). Steps 4–5 = the student who did the analysis. |
| Slides (.pptx) | Slide 1 | Student 1 name, Student 2 name |

After filling them in, **remove the yellow highlight** (select all → Highlight → No Color).

---

## Folder map

```
00_Original_Files/      Original files as received (brief, Fawaz's drafts, CourseWork.zip). Do not submit these.
01_Final_Report/        ✅ FINAL report (.docx + .pdf) and its 3 figures
02_Presentation/        ✅ FINAL slides (.pptx + .pdf) + Speaker_Script.md for the recording
03_Explainer_Page/      📖 HTML explainer, for the team only (not for submission)
04_Evidence/            Original evidence: 2 PCAPs, PLC audit log, console log, SHA256SUMS.txt, 20 screenshots
05_Analysis/            Our analysis script (correlate_evidence.py) and the tshark + script outputs
06_Lab_Setup/           quick_lab.py (software PLC) + LAB_GUIDE.md (how the lab was built)
```

## Key facts to remember (in case the instructor asks)

- **Lab:** two Ubuntu VMs, OT-PLC `10.20.30.10:1502` and OT-CLIENT `10.20.30.20`, on the VirtualBox internal network `OTLAB`. Run date: 26 Oct 2026.
- **The write:** `incident.pcap` frame 14, 16:31:30.220 UTC, bytes `00 01 00 00 00 06 01 06 00 10 00 5A` = function 06 (write), register 16, value 90.
- **Corroboration:** PLC echo in frame 16 (+6.9 ms) → audit log `WRITE_APPLIED 50→90` (+3.5 ms more) → read-back = 90 in frame 26.
- **Negative control:** `baseline.pcap` has 0 write commands.
- **Validation:** tshark and our own Python decoder give identical results; the hashes all still match.
- **Tool finding:** tshark shows "Unable to classify as query or response" on port 1502. The fix is `-o mbtcp.tcp.port:1502`.
- **Limit:** we can prove a **host**, not a **person** (Modbus has no users). The packets and the log share one clock.

## Re-running the analysis (optional)

```bash
cd 04_Evidence/Evidence_Artifacts
sha256sum -c SHA256SUMS.txt
python3 ../../05_Analysis/correlate_evidence.py .
tshark -r incident.pcap -o mbtcp.tcp.port:1502 -Y modbus
```

## Points to confirm with Fawaz before submitting

1. **Internet (NAT) adapter:** VirtualBox shows Adapter 1 as "NAT Network". Was it disabled during the capture? The report does not claim either way. It only says that the traffic was on the internal network `OTLAB`.
2. **Chain of custody:** confirm the steps in Appendix B, Table B2 (who archived the files, and when the zip was sent).
3. **Keep the VMs:** the brief says the instructor may ask for the original files. Do not delete the VMs or `~/sec524_run1` until grades are out.
4. **Historian:** the lab guide mentions `historian.py`, but it was never run and is not in the repo. The report says it was "not deployed". Confirm that this is correct.
5. **AI-use statement:** Appendix E of the report contains a short AI-use statement, because Section 9 of the coursework brief asks for permitted AI use to be disclosed. Check the course policy and keep or adjust the wording.

---

## الملخص بالعربي

**ما هو المشروع؟** تحقيق جنائي رقمي في أنظمة التحكم الصناعي (OT). في مختبر افتراضي، غيّر شخص قيمة في جهاز PLC من 50 إلى 90 بدون إذن. المطلوب إثبات ما حدث من خلال تسجيلات الشبكة وسجل الـ PLC.

**الحالة:** التقرير والعرض والملفات الداعمة كلها جاهزة. بقي فقط كتابة الأسماء.

**ماذا تفعل الآن؟**
1. **افهم المشروع أولاً:** حمّل ملف `03_Explainer_Page/SEC524_Project_Explained.html` وافتحه في المتصفح، واضغط زر **عربي** في الأعلى.
2. **اكتب الأسماء:** كل مكان يحتاج تعبئة **مُظلَّل باللون الأصفر**:
   - التقرير (ملف Word): الصفحة الأولى (اسم الطالبين وأرقامهما الجامعية واسم الدكتور)، والملحق B جدول B2 (سلسلة الحيازة).
   - العرض (PowerPoint): الشريحة الأولى.
   - بعد التعبئة احذف اللون الأصفر.
3. **حوّل التقرير إلى PDF** من Word، لأن المقرر يطلب PDF.
4. **سجّل العرض (10 دقائق):** نص الإلقاء موجود داخل ملف PowerPoint (Notes) وفي ملف `02_Presentation/Speaker_Script.md`. مدته حوالي 9.3 دقائق.
5. **ارفع على Blackboard:** ملف PDF للتقرير، والفيديو، والملفات الداعمة (المجلدات 04 و 05 و 06 مضغوطة).

**أمور تُناقَش مع فواز قبل التسليم:**
1. هل كان محوّل الإنترنت (NAT) مُطفأً أثناء التجربة؟ التقرير لا يقول شيئاً عن هذه النقطة.
2. التأكد من خطوات سلسلة الحيازة في الملحق B.
3. عدم حذف الأجهزة الافتراضية حتى صدور الدرجات، لأن الدكتور قد يطلب الملفات الأصلية.
4. التأكد أن جهاز الـ historian لم يُشغَّل فعلاً، كما هو مكتوب في التقرير.
5. في الملحق E يوجد سطر للإفصاح عن استخدام الذكاء الاصطناعي، لأن ملف المتطلبات (القسم 9) يطلب ذلك. راجعوا سياسة المقرر وقرّروا الصياغة.
