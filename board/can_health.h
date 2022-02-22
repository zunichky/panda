// When changing this struct, boardd and python/__init__.py needs to be kept up to date!
#define CAN_HEALTH_PACKET_VERSION 1
struct __attribute__((packed)) can_health_t {
  uint8_t ecr_cel_pkt;
  uint8_t ecr_rp_pkt;
  uint8_t ecr_rec_pkt;
  uint8_t ecr_tec_pkt;
  uint8_t psr_pxe_pkt;
  uint8_t psr_redl_pkt;
  uint8_t psr_rbrs_pkt;
  uint8_t psr_resi_pkt;
  uint8_t psr_dlec_pkt;
  uint8_t psr_bo_pkt;
  uint8_t psr_ew_pkt;
  uint8_t psr_ep_pkt;
  uint8_t psr_act_pkt;
  uint8_t psr_lec_pkt;
};
