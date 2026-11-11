# Speaker Script – SEC 524 OT Forensics (10-minute recording)
Read this while showing the slides. The same text is inside the PowerPoint as speaker notes (View → Notes). About 45 seconds per slide.

Total: 1215 words, which is about 9.3 minutes at a normal speaking pace of 130 words per minute.

## Slide 1 – Title slide

Welcome. In this talk we present our SEC 524 coursework on Operational Technology forensics. We took one concrete problem: somebody changes a setpoint inside a PLC over the Modbus protocol, without approval. We wanted to see what an investigator can really prove in that case, and what stays unknown. We built a small virtual lab, ran a controlled incident, collected and preserved the evidence, and reconstructed what happened. In about ten minutes we will cover the problem, the forensic challenges, our framework, the experiment, the findings and the limits.

## Slide 2 – The forensic problem

Here is the problem. In our scenario, register 16 of a PLC is a process setpoint. Its normal value is 50. Someone changed it to 90, and there was no approved change request. MITRE lists this as technique T0836, Modify Parameter. But as investigators we have to be careful: the same Modbus bytes could come from a technician, an HMI script or a scheduled task. So our question is not only "did it happen". It is which command was sent, from where, when, whether the PLC accepted it, and what we cannot say about who did it.

## Slide 3 – Why OT forensics is different

Why is OT harder than normal computer forensics? First, you cannot just switch a PLC off and image it, because it controls a real process, so evidence is collected live and passively. Second, Modbus has no concept of a user. A packet tells us an IP address and port, never a person. Third, safety comes before evidence. Sending scans or test commands to a live controller can damage equipment, so every action must be approved by the plant owner. These three points shaped both our framework and our lab design.

## Slide 4 – Evidence sources and what they can prove

This slide lists the evidence sources for this kind of incident, from most to least volatile. The PLC state and the network traffic are the most fragile: if nobody captures the packets live, they are gone. The PLC audit log is the best source to show whether the controller actually applied the change. The workstation is where you could link an IP to an account. Historian trends show physical effect. The order matters because collecting slow sources first can cost you the fragile ones.

## Slide 5 – Key forensic challenges

Four challenges matter most. Attribution: an IP address is not an account, and an account is not a person. Time: PLC clocks drift and historians sample, so if we do not normalise to UTC and measure offsets, we can put events in the wrong order. Tools: vendor formats are closed, and even Wireshark mislabelled our own traffic because we used port 1502; we will come back to this. Anti-forensics: an attacker can delete logs or write the value back. The answers are remote log forwarding, NTP and passive monitoring.

## Slide 6 – Our OT-adapted forensic framework

Our framework starts from the NIST SP 800-86 process and the OSCAR model from the course. Both assume that collecting evidence is low-risk, which is not true in OT. So we built 13 stages in four phases. The orange boxes are our changes. Stage 1 adds a safety gate signed off by the plant owner. Stage 3 ranks sources by process risk as well as volatility. Stage 5 is passive first. Stage 7 adds protocol semantics, meaning a register number is linked to its engineering meaning. Stage 9 records the clock and offset of every source. Stage 10 forces us to test competing hypotheses. Stage 13 feeds lessons back into readiness.

## Slide 7 – Our virtual OT lab

This is the lab. Two Ubuntu virtual machines in VirtualBox, connected only through a private internal network called OTLAB. OT-PLC runs a small Python Modbus server that holds register 16, value 50, and logs every request. OT-CLIENT plays the engineering workstation. We used port 1502 so the server did not need root. The run was on 26 October 2026. First a baseline capture with three reads only, as a negative control. Then the incident capture: read, write 90, read. We stopped the writers, hashed the four evidence files, and analysed only verified copies.

## Slide 8 – Evidence collected and preserved

These are our four evidence items. E1 and E2 are the packet captures, 30 frames each. E3 is the PLC audit log with six records, one of them WRITE_APPLIED. E4 is the console copy. Every file was hashed with SHA-256 on the PLC VM, then the folder was archived and passed to the second team member, who re-verified all four hashes before any analysis. One important point: a matching hash proves the copy is unchanged since hashing. It does not prove that the capture caught everything.

## Slide 9 – The write, byte by byte

This is the actual write command from frame 14. The first seven bytes are the MBAP header: transaction ID 1, protocol 0, length 6, unit 1. Then the PDU: function code 06 means write single register, 0010 hex is register 16, and 005A hex is 90. Three independent views confirm it. The network capture shows the request, and frame 16 shows the PLC echoing it back, which in Modbus means accepted. The PLC audit log records WRITE_APPLIED from 50 to 90. And a read 3.7 seconds later returns 90. All three agree.

## Slide 10 – Timeline and validation

The timeline zooms in on the write. The request is at 16:31:30.220. The PLC echo comes 6.9 milliseconds later. The audit log line comes 3.5 milliseconds after that, because the simulator replies first and then writes the log. We validated in three ways. Two decoders, tshark and our own Python script, gave identical results. Two evidence types, packets and log, agree on every event. And because we ran the incident ourselves, we know the ground truth, and it matches. We also found a tool issue: on port 1502 tshark could not label query and response until we set the Modbus port preference.

## Slide 11 – What we can and cannot say

Now the most important slide for an investigator: what we can and cannot say. Observed facts: the write of 90 to register 16 came from 10.20.30.20, the PLC accepted it and its state changed, so hypotheses one and two are supported. Reasonable inferences: the command came from the OT-CLIENT VM, and it was unauthorised, but only because our case notes say no change was approved; that is how we reject H4. Unknowns: who typed it. Modbus has no user identity, and we did not collect workstation logs, so H3 is not supported. The evidence points to a host, not a person.

## Slide 12 – Limitations, legal context and readiness

Our limitations: the packet capture and the log share one clock, so they are consistent but not independently timed. The capture was on the PLC itself, the PLC is a teaching simulator, we have no workstation evidence, and the dataset is small. On the legal side, in Saudi Arabia the Anti-Cyber Crime Law applies to unauthorised interference, the PDPL protects employee data in logs, and NCA OT controls apply to in-scope operators. To be ready for a real incident: a passive TAP, off-box logging, one NTP source, a register map with change tickets, and named accounts with MFA on engineering hosts.

## Slide 13 – Conclusion

To conclude. First, an unauthorised PLC setpoint change can be reconstructed with confidence when packets and controller logs are preserved and correlated; our three views and two decoders agree with the ground truth. Second, the conclusion has a clear boundary: we can prove a host and an accepted command, not a person. Third, our adapted framework keeps the core of NIST and OSCAR but adds a safety gate, passive-first collection, protocol semantics and explicit clock handling. Thank you for listening.
