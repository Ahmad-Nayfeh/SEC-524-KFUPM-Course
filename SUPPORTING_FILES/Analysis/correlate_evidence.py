"""SEC 524 - independent check of the Modbus/TCP evidence.

Reads the raw PCAP bytes without Wireshark, decodes every Modbus/TCP PDU,
and lines each one up with the PLC audit log (plc_audit.jsonl).
This gives a second technique next to the tshark decode.

Usage:
    python3 correlate_evidence.py <evidence_folder>

Only the Python standard library is used, so the result does not depend on
the Wireshark dissector.
"""
import datetime as dt
import hashlib
import json
import struct
import sys
from pathlib import Path

PORT = 1502
FUNC = {3: 'READ (FC03)', 6: 'WRITE (FC06)'}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def utc(ts):
    return dt.datetime.fromtimestamp(ts, dt.timezone.utc)


def read_pcap(path):
    """Yield (frame_no, timestamp, src, sport, dst, dport, payload) for TCP/IPv4 frames."""
    data = path.read_bytes()
    magic = struct.unpack('<I', data[:4])[0]
    if magic != 0xA1B2C3D4:
        raise ValueError(f'{path.name}: unexpected pcap magic {magic:#x}')
    off, n = 24, 0
    while off < len(data):
        sec, usec, incl, _ = struct.unpack('<IIII', data[off:off + 16])
        frame = data[off + 16: off + 16 + incl]
        off += 16 + incl
        n += 1
        if struct.unpack('>H', frame[12:14])[0] != 0x0800:   # Ethernet -> IPv4 only
            continue
        ip = frame[14:]
        ihl = (ip[0] & 0x0F) * 4
        if ip[9] != 6:                                       # TCP only
            continue
        src, dst = '.'.join(map(str, ip[12:16])), '.'.join(map(str, ip[16:20]))
        tcp = ip[ihl:]
        sport, dport = struct.unpack('>HH', tcp[:4])
        payload = tcp[(tcp[12] >> 4) * 4:]
        yield n, sec + usec / 1e6, src, sport, dst, dport, payload


def modbus_events(path):
    events = []
    for n, ts, src, sport, dst, dport, pl in read_pcap(path):
        if len(pl) < 8 or PORT not in (sport, dport):
            continue
        tid, proto, length, unit = struct.unpack('>HHHB', pl[:7])
        pdu = pl[7:6 + length]
        direction = 'request' if dport == PORT else 'response'
        fc = pdu[0]
        if fc == 3 and direction == 'request':
            detail = f'register {struct.unpack(">H", pdu[1:3])[0]}, count {struct.unpack(">H", pdu[3:5])[0]}'
        elif fc == 3:
            detail = f'value {struct.unpack(">H", pdu[2:4])[0]}'
        elif fc == 6:
            reg, val = struct.unpack('>HH', pdu[1:5])
            detail = f'register {reg}, value {val}'
        else:
            detail = pdu.hex()
        events.append(dict(file=path.name, frame=n, ts=ts, src=src, sport=sport, dst=dst,
                           tid=tid, unit=unit, fc=fc, direction=direction, detail=detail,
                           raw=pl.hex()))
    return events


def main(folder):
    folder = Path(folder)
    print('== 1. Integrity check against SHA256SUMS.txt')
    for line in (folder / 'SHA256SUMS.txt').read_text().split('\n'):
        if line.strip():
            digest, name = line.split()
            ok = sha256(folder / name) == digest
            print(f'  {name:18} {"OK" if ok else "MISMATCH"}  {digest[:16]}...')

    print('\n== 2. Modbus PDUs decoded from raw PCAP bytes')
    pkts = modbus_events(folder / 'baseline.pcap') + modbus_events(folder / 'incident.pcap')
    for e in pkts:
        print(f"  {e['file']:14} #{e['frame']:<3} {utc(e['ts']).strftime('%H:%M:%S.%f')}  "
              f"{e['src']}:{e['sport']:<5} {e['direction']:8} TID={e['tid']} unit={e['unit']} "
              f"{FUNC.get(e['fc'], e['fc'])}: {e['detail']}   [{e['raw']}]")
    writes = [e for e in pkts if e['fc'] == 6]
    print(f"\n  FC06 frames in baseline.pcap: {sum(e['file'] == 'baseline.pcap' for e in writes)}")
    print(f"  FC06 frames in incident.pcap: {sum(e['file'] == 'incident.pcap' for e in writes)}")

    print('\n== 3. Correlation: each PLC audit record vs the nearest response packet')
    log = [json.loads(l) for l in (folder / 'plc_audit.jsonl').read_text().splitlines() if l]
    responses = [e for e in pkts if e['direction'] == 'response']
    requests = [e for e in pkts if e['direction'] == 'request']
    for rec in log:
        t = dt.datetime.fromisoformat(rec['time_utc']).timestamp()
        resp = min(responses, key=lambda e: abs(e['ts'] - t))
        req = max((e for e in requests if e['ts'] <= t), key=lambda e: e['ts'])
        print(f"  {rec['time_utc'][11:26]} {rec['event']:13} {rec['before']}->{rec['after']:<3} | "
              f"request {req['file']}#{req['frame']} at +{(t - req['ts']) * 1000:6.2f} ms, "
              f"response #{resp['frame']} at {(t - resp['ts']) * 1000:+6.2f} ms, "
              f"IP match={rec['client_ip'] == req['src']}")


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '.')
