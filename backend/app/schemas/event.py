from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class NetworkFlowRaw(BaseModel):
    """Raw network flow payload emitted by Kafka/Redis stream producer."""
    flow_id: Optional[str] = None
    timestamp: Optional[datetime] = None
    src_ip: str
    dst_ip: str
    src_port: int = Field(..., ge=0, le=65535)
    dst_port: int = Field(..., ge=0, le=65535)
    protocol: str = "TCP"
    
    # CICIDS2018 core flow statistics
    flow_duration: float = 0.0
    tot_fwd_pkts: int = 0
    tot_bwd_pkts: int = 0
    totlen_fwd_pkts: float = 0.0
    totlen_bwd_pkts: float = 0.0
    fwd_pkt_len_max: float = 0.0
    fwd_pkt_len_min: float = 0.0
    fwd_pkt_len_mean: float = 0.0
    bwd_pkt_len_max: float = 0.0
    bwd_pkt_len_min: float = 0.0
    bwd_pkt_len_mean: float = 0.0
    flow_byts_s: float = 0.0
    flow_pkts_s: float = 0.0
    flow_iat_mean: float = 0.0
    flow_iat_std: float = 0.0
    flow_iat_max: float = 0.0
    flow_iat_min: float = 0.0
    fwd_iat_tot: float = 0.0
    bwd_iat_tot: float = 0.0
    fwd_psh_flags: int = 0
    bwd_psh_flags: int = 0
    fwd_urg_flags: int = 0
    bwd_urg_flags: int = 0
    fwd_header_len: int = 0
    bwd_header_len: int = 0
    fwd_pkts_s: float = 0.0
    bwd_pkts_s: float = 0.0
    pkt_len_min: float = 0.0
    pkt_len_max: float = 0.0
    pkt_len_mean: float = 0.0
    pkt_len_std: float = 0.0
    pkt_len_var: float = 0.0
    fin_flag_cnt: int = 0
    syn_flag_cnt: int = 0
    rst_flag_cnt: int = 0
    psh_flag_cnt: int = 0
    ack_flag_cnt: int = 0
    urg_flag_cnt: int = 0
    down_up_ratio: float = 0.0
    init_fwd_win_byts: int = 0
    init_bwd_win_byts: int = 0
    
    # Ground truth (if replaying labeled dataset)
    true_label: Optional[str] = None

class EventResponse(BaseModel):
    id: int
    timestamp: datetime
    src_ip: str
    dst_ip: str
    src_port: Optional[int]
    dst_port: int
    protocol: str
    flow_duration: float
    tot_fwd_pkts: int
    tot_bwd_pkts: int
    tot_bytes: int
    prediction: str
    confidence: float
    anomaly_score: float
    is_anomaly: bool
    inference_latency_ms: float
    extra_features: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)
