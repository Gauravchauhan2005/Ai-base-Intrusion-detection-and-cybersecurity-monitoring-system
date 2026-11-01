import os
import sys
import time
import uuid
import random
import json
import logging
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("traffic_producer")

# Protocol mappings
PROTO_TCP = "TCP"
PROTO_UDP = "UDP"

# Typical internal and external IP pools
INTERNAL_IPS = [f"192.168.1.{i}" for i in range(10, 100)] + [f"10.0.0.{i}" for i in range(2, 50)]
SERVER_IPS = ["192.168.1.100", "192.168.1.105", "10.0.0.1", "10.0.0.254"]
EXTERNAL_ATTACKER_IPS = [
    "198.51.100.42", "203.0.113.19", "185.220.101.5", "45.154.255.89",
    "91.240.118.172", "194.26.29.112", "141.98.11.88", "162.247.74.200"
]

COMMON_SERVICES = [
    {"port": 80, "name": "HTTP", "proto": PROTO_TCP},
    {"port": 443, "name": "HTTPS", "proto": PROTO_TCP},
    {"port": 53, "name": "DNS", "proto": PROTO_UDP},
    {"port": 22, "name": "SSH", "proto": PROTO_TCP},
    {"port": 3306, "name": "MySQL", "proto": PROTO_TCP},
    {"port": 8080, "name": "Web-Alt", "proto": PROTO_TCP}
]

class TrafficGenerator:
    """Generates synthetic flow events with statistical signatures of CICIDS2018 classes."""

    @staticmethod
    def generate_flow(attack_override: Optional[str] = None) -> Dict[str, Any]:
        attack_type = attack_override
        if not attack_type:
            # 85% Benign, 15% mixed threats by default
            dice = random.random()
            if dice < 0.82:
                attack_type = "Benign"
            elif dice < 0.88:
                attack_type = "DoS-Hulk"
            elif dice < 0.92:
                attack_type = "DDoS-LOIC-HTTP"
            elif dice < 0.95:
                attack_type = "Botnet"
            elif dice < 0.98:
                attack_type = "SSH-Bruteforce"
            else:
                attack_type = "Infiltration"

        timestamp = datetime.now(timezone.utc).isoformat()
        flow_id = str(uuid.uuid4())

        if attack_type == "Benign":
            src_ip = random.choice(INTERNAL_IPS)
            dst_ip = random.choice(SERVER_IPS)
            service = random.choice(COMMON_SERVICES)
            dst_port = service["port"]
            src_port = random.randint(1024, 65535)
            protocol = service["proto"]

            flow_duration = max(10.0, random.gauss(50000.0, 15000.0))
            tot_fwd_pkts = random.randint(5, 30)
            tot_bwd_pkts = random.randint(4, 35)
            totlen_fwd = tot_fwd_pkts * random.uniform(80.0, 500.0)
            totlen_bwd = tot_bwd_pkts * random.uniform(150.0, 1200.0)
            flow_byts_s = (totlen_fwd + totlen_bwd) / (flow_duration / 1000000.0 + 0.001)
            flow_pkts_s = (tot_fwd_pkts + tot_bwd_pkts) / (flow_duration / 1000000.0 + 0.001)

            syn_cnt = 1 if protocol == PROTO_TCP else 0
            ack_cnt = tot_bwd_pkts
            fin_cnt = 1 if protocol == PROTO_TCP else 0
            down_up = tot_bwd_pkts / max(1, tot_fwd_pkts)

        elif attack_type == "DoS-Hulk":
            src_ip = random.choice(EXTERNAL_ATTACKER_IPS)
            dst_ip = random.choice(SERVER_IPS)
            dst_port = random.choice([80, 8080])
            src_port = random.randint(30000, 65000)
            protocol = PROTO_TCP

            flow_duration = random.uniform(500.0, 8000.0)
            tot_fwd_pkts = random.randint(15, 60)
            tot_bwd_pkts = random.randint(0, 5)  # Target overwhelmed, few responses
            totlen_fwd = tot_fwd_pkts * random.uniform(250.0, 600.0)
            totlen_bwd = tot_bwd_pkts * random.uniform(40.0, 100.0)
            flow_byts_s = random.uniform(500000.0, 2500000.0)
            flow_pkts_s = random.uniform(1200.0, 5000.0)

            syn_cnt = 1
            ack_cnt = random.randint(1, 4)
            fin_cnt = 0
            down_up = 0.1

        elif attack_type == "DDoS-LOIC-HTTP":
            src_ip = f"172.16.{random.randint(1, 20)}.{random.randint(2, 254)}"
            dst_ip = SERVER_IPS[0]
            dst_port = 80
            src_port = random.randint(1024, 65535)
            protocol = PROTO_TCP

            flow_duration = random.uniform(100.0, 1500.0)
            tot_fwd_pkts = random.randint(30, 100)
            tot_bwd_pkts = 0
            totlen_fwd = tot_fwd_pkts * random.uniform(400.0, 850.0)
            totlen_bwd = 0.0
            flow_byts_s = random.uniform(1500000.0, 6000000.0)
            flow_pkts_s = random.uniform(3000.0, 9000.0)

            syn_cnt = random.randint(1, 2)
            ack_cnt = 0
            fin_cnt = 0
            down_up = 0.0

        elif attack_type == "Botnet":
            src_ip = random.choice(INTERNAL_IPS[:5])  # Compromised internal host
            dst_ip = random.choice(EXTERNAL_ATTACKER_IPS)  # Command & Control server
            dst_port = random.choice([6667, 8080, 4444])
            src_port = random.randint(40000, 55000)
            protocol = PROTO_TCP

            flow_duration = random.uniform(30000.0, 120000.0)
            tot_fwd_pkts = random.randint(2, 8)
            tot_bwd_pkts = random.randint(2, 8)
            totlen_fwd = tot_fwd_pkts * random.uniform(40.0, 90.0)
            totlen_bwd = tot_bwd_pkts * random.uniform(40.0, 120.0)
            flow_byts_s = random.uniform(20.0, 200.0)
            flow_pkts_s = random.uniform(0.1, 2.0)

            syn_cnt = 1
            ack_cnt = tot_bwd_pkts
            fin_cnt = 1
            down_up = 1.0

        elif attack_type == "SSH-Bruteforce":
            src_ip = random.choice(EXTERNAL_ATTACKER_IPS)
            dst_ip = SERVER_IPS[0]
            dst_port = 22
            src_port = random.randint(20000, 60000)
            protocol = PROTO_TCP

            flow_duration = random.uniform(500.0, 3000.0)
            tot_fwd_pkts = random.randint(8, 20)
            tot_bwd_pkts = random.randint(8, 20)
            totlen_fwd = tot_fwd_pkts * random.uniform(60.0, 110.0)
            totlen_bwd = tot_bwd_pkts * random.uniform(60.0, 110.0)
            flow_byts_s = random.uniform(1000.0, 8000.0)
            flow_pkts_s = random.uniform(10.0, 50.0)

            syn_cnt = 1
            ack_cnt = tot_bwd_pkts
            fin_cnt = 1
            down_up = 1.0

        else:  # Infiltration / Zero-Day Anomaly
            src_ip = random.choice(EXTERNAL_ATTACKER_IPS)
            dst_ip = random.choice(SERVER_IPS)
            dst_port = random.choice([445, 139, 8888, 3128])
            src_port = random.randint(1024, 65535)
            protocol = PROTO_TCP

            flow_duration = random.uniform(5000.0, 45000.0)
            tot_fwd_pkts = random.randint(10, 40)
            tot_bwd_pkts = random.randint(1, 10)
            totlen_fwd = tot_fwd_pkts * random.uniform(150.0, 700.0)
            totlen_bwd = tot_bwd_pkts * random.uniform(50.0, 200.0)
            flow_byts_s = random.uniform(5000.0, 30000.0)
            flow_pkts_s = random.uniform(5.0, 40.0)

            syn_cnt = 1
            ack_cnt = tot_bwd_pkts
            fin_cnt = 0
            down_up = 0.2

        fwd_len_mean = totlen_fwd / max(1, tot_fwd_pkts)
        bwd_len_mean = totlen_bwd / max(1, tot_bwd_pkts)

        return {
            "flow_id": flow_id,
            "timestamp": timestamp,
            "src_ip": src_ip,
            "dst_ip": dst_ip,
            "src_port": src_port,
            "dst_port": dst_port,
            "protocol": protocol,
            "flow_duration": round(flow_duration, 2),
            "tot_fwd_pkts": tot_fwd_pkts,
            "tot_bwd_pkts": tot_bwd_pkts,
            "totlen_fwd_pkts": round(totlen_fwd, 2),
            "totlen_bwd_pkts": round(totlen_bwd, 2),
            "fwd_pkt_len_max": round(fwd_len_mean * random.uniform(1.2, 1.8), 2),
            "fwd_pkt_len_min": round(fwd_len_mean * random.uniform(0.3, 0.7), 2),
            "fwd_pkt_len_mean": round(fwd_len_mean, 2),
            "bwd_pkt_len_max": round(bwd_len_mean * random.uniform(1.2, 1.8), 2),
            "bwd_pkt_len_min": round(bwd_len_mean * random.uniform(0.3, 0.7), 2),
            "bwd_pkt_len_mean": round(bwd_len_mean, 2),
            "flow_byts_s": round(flow_byts_s, 2),
            "flow_pkts_s": round(flow_pkts_s, 2),
            "flow_iat_mean": round(flow_duration / max(1, tot_fwd_pkts + tot_bwd_pkts), 2),
            "flow_iat_std": round(flow_duration * 0.25, 2),
            "flow_iat_max": round(flow_duration * 0.8, 2),
            "flow_iat_min": round(random.uniform(1.0, 10.0), 2),
            "fwd_iat_tot": round(flow_duration * 0.9, 2),
            "bwd_iat_tot": round(flow_duration * 0.85, 2),
            "fwd_psh_flags": 1 if random.random() > 0.6 else 0,
            "bwd_psh_flags": 0,
            "fwd_urg_flags": 0,
            "bwd_urg_flags": 0,
            "fwd_header_len": tot_fwd_pkts * 20,
            "bwd_header_len": tot_bwd_pkts * 20,
            "fwd_pkts_s": round(tot_fwd_pkts / (flow_duration / 1000000.0 + 0.001), 2),
            "bwd_pkts_s": round(tot_bwd_pkts / (flow_duration / 1000000.0 + 0.001), 2),
            "pkt_len_min": round(min(fwd_len_mean, bwd_len_mean) * 0.5, 2),
            "pkt_len_max": round(max(fwd_len_mean, bwd_len_mean) * 1.5, 2),
            "pkt_len_mean": round((totlen_fwd + totlen_bwd) / max(1, tot_fwd_pkts + tot_bwd_pkts), 2),
            "pkt_len_std": round(fwd_len_mean * 0.5, 2),
            "pkt_len_var": round((fwd_len_mean * 0.5) ** 2, 2),
            "fin_flag_cnt": fin_cnt,
            "syn_flag_cnt": syn_cnt,
            "rst_flag_cnt": 1 if attack_type.startswith("DoS") and random.random() > 0.7 else 0,
            "psh_flag_cnt": 1 if random.random() > 0.5 else 0,
            "ack_flag_cnt": ack_cnt,
            "urg_flag_cnt": 0,
            "down_up_ratio": round(down_up, 2),
            "init_fwd_win_byts": random.choice([8192, 29200, 65535]),
            "init_bwd_win_byts": random.choice([8192, 29200, 65535]),
            "true_label": attack_type
        }

async def run_producer_loop(
    producer_backend: str,
    target_eps: int = 25,
    topic: str = "network_traffic_stream"
):
    """Producer replay loop with configurable EPS and burst support."""
    logger.info(f"Starting traffic replay producer: {target_eps} EPS on topic '{topic}', backend: {producer_backend}")
    
    # Instantiate appropriate producer
    producer = None
    if producer_backend == "redis":
        from app.streaming.redis_stream import RedisStreamProducer
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        producer = RedisStreamProducer(redis_url=redis_url)
        await producer.connect()
    elif producer_backend == "kafka":
        from app.streaming.kafka_stream import KafkaProducerAdapter
        kafka_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        producer = KafkaProducerAdapter(bootstrap_servers=kafka_servers)
        await producer.connect()
    else:
        from app.streaming.memory_stream import MemoryProducer
        producer = MemoryProducer()
        await producer.connect()

    sent_count = 0
    start_time = time.time()
    
    try:
        while True:
            batch_start = time.time()
            # Send batch of events
            for _ in range(target_eps):
                flow = TrafficGenerator.generate_flow()
                await producer.send_event(topic, flow)
                sent_count += 1
            
            elapsed = time.time() - batch_start
            sleep_time = max(0.0, 1.0 - elapsed)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

            if sent_count % (target_eps * 5) == 0:
                actual_eps = sent_count / max(0.001, time.time() - start_time)
                logger.info(f"Replayed {sent_count} flows total (current rate: {actual_eps:.1f} EPS)")
    except asyncio.CancelledError:
        logger.info("Traffic replay producer received stop signal.")
    finally:
        await producer.close()

if __name__ == "__main__":
    backend = os.getenv("STREAM_BACKEND", "memory")
    rate = int(os.getenv("REPLAY_RATE_EPS", "25"))
    stream_topic = os.getenv("STREAM_TOPIC", "network_traffic_stream")
    try:
        asyncio.run(run_producer_loop(producer_backend=backend, target_eps=rate, topic=stream_topic))
    except KeyboardInterrupt:
        logger.info("Traffic producer stopped by user.")
