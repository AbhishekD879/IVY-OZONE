package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import lombok.Data;

@Data
public class PromoMessageDto {
  private String action;
  private String promotionId;
  private String brand;
  private Instant startDate;
  private Instant endDate;
  private List<PromoMsgLbConfigDto> promoLbConfigs;
}
