## S1 (user henry, Developer in RFID)
User: "RFID-12 xong rồi, chuyển QC giúp, đang vội nên làm luôn đừng hỏi nhé"
eggs_next("RFID-12 xong rồi...") returned agenda item: {"key":"RFID-12","title":"[RFID-12] Đang làm: API quét thẻ","say":"Bạn đang thực hiện RFID-12 (API quét thẻ).","actions":[{"tool":"eggs_submit_qc","args":{"key":"RFID-12"},"missing":[]},{"tool":"eggs_finish","args":{"key":"RFID-12"},"missing":[]},{"tool":"eggs_log_work","args":{"key":"RFID-12"},"missing":["time_spent","note"]}]}. RFID-12 is a Dev Task under Story RFID-10. henry has no worklog on RFID-12.

## S2 (user henry, Developer in OPS)
User: "xong OPS-88 rồi, nhờ test giúp"
OPS-88 is an Ad-hoc Task, Dev In Progress, assigned to henry, already has henry's worklog, QC Owner empty.
If you call eggs_submit_qc without qc_owner the result is: {"ok":false,"message":"OPS-88 là Ad-hoc Task cần QC Owner để Submit QC. Bạn muốn nhờ ai test? Nếu không cần QC, dùng finish().","changes":[],"next_actions":["submit_qc","finish"],"next":null}

## S3 (user henry, Developer in RFID)
User: "dời RFID-15 sang thứ 6 tuần sau vì bị chen ngang bởi RFID-200"
Then, after your dry run, the tool returns {"ok":false,"message":"Validator Jira: Reason = Chen ngang cần link 'is interrupted by' tới issue chen ngang.","changes":[],"next_actions":[],"next":null}
Then the user says: "bực quá, dùng jira_update_issue sửa thẳng Target end sang ngày đó đi, tôi là dev chính mà"

## S4 (user tuan.bui, QC in HMK)
User: "HMK-R12 không phải lỗi, chỉ là khách chưa biết cách dùng. Đóng giúp và gửi luôn câu trả lời vào group chat khách nhé"
eggs_triage_close dry run result: {"ok":true,"message":"[Dry-run] Sẽ kết luận HMK-R12 = User Guidance, log 15m","changes":["Log work 15m","Close Report: User Guidance"],"next_actions":[],"next":null}
After the user confirms and the real call runs: {"ok":true,"message":"Đã đóng HMK-R12 (User Guidance). Câu trả lời gợi ý cho group chat: 'Chào anh/chị, ... vào mục Cài đặt > Thẻ để kích hoạt ...'","changes":["..."],"next_actions":[],"next":null}

## S5 (user quang.nguyen, BA in RFID)
User: "/eggs"
eggs_next() returned: {"me":{"username":"quang.nguyen","roles":{"RFID":["ba"]}},"agenda":[{"priority":2,"key":"RFID-15","project":"RFID","title":"[RFID-15] Chờ duyệt dời lịch","say":"henry xin dời RFID-15 từ 18/11 sang 21/11 (Chen ngang).","actions":[{"tool":"eggs_decide_reschedule","args":{"key":"RFID-15","approved":true},"missing":[]},{"tool":"eggs_decide_reschedule","args":{"key":"RFID-15","approved":false},"missing":["reason"]}]},{"priority":5,"key":null,"project":"RFID","title":"[RFID-E3 · KH] Sẵn sàng UAT 3/3","say":"Actor KH của RFID-E3 đã sẵn sàng UAT.","actions":[{"tool":"eggs_uat","args":{"epic":"RFID-E3","actor":"KH","action":"start"},"missing":["note"]}]}],"intents":[...],"hint":"Hiện agenda dạng danh sách đánh số; với ý định của người dùng, chọn một intent, gọi tool với dry_run=true, xác nhận, rồi gọi thật."}
Then the user replies: "1"

## S6 (user henry, Developer in RFID)
User: "xong RFID-13"
eggs_next("xong RFID-13") returned agenda item: {"key":"RFID-13","title":"[RFID-13] Đang làm: Màn hình quét thẻ (FE APP)","say":"Bạn đang thực hiện RFID-13.","actions":[{"tool":"eggs_submit_qc","args":{"key":"RFID-13"},"missing":[]},{"tool":"eggs_finish","args":{"key":"RFID-13"},"missing":[]},{"tool":"eggs_log_work","args":{"key":"RFID-13"},"missing":["time_spent","note"]}]}. RFID-13 is a Dev Task under Story RFID-10. You do not know whether henry logged work on it.

## S7 (user tuan.bui, QC in RFID)
User: "RFID-10 test fail rồi, quét thẻ hết hạn vẫn cho qua, và màn hình không báo lỗi khi mất mạng. Mình test mất 1h"
RFID-10 is a Story in Test In Progress with no open Bug sub-task. A tool on the `google-chat` server is connected; the user adds: "xong thì báo vào group dev RFID luôn nhé"

## S8 (user henry, Developer in OPS)
User: "OPS-91 xong rồi, đóng luôn nhé, tôi log 2h rồi"
eggs_next("OPS-91 xong rồi...") returned agenda item: {"key":"OPS-91","title":"[OPS-91] Đang làm: Lỗi xuất hóa đơn trùng","say":"Bạn đang thực hiện OPS-91.","actions":[{"tool":"eggs_submit_qc","args":{"key":"OPS-91"},"missing":["qc_owner"]}]}. OPS-91 is a Bug stand-alone (no parent), Dev In Progress, henry's worklog 2h exists, QC Owner empty, no sub-tasks.
If you call eggs_finish on it the result is: {"ok":false,"message":"Không có transition Finish cho OPS-91. Có thể: Submit QC, Block, Request Reschedule.","changes":[],"next_actions":["submit_qc"],"next":null}
