package com.entain.oxygen.promosandbox.dto;

import java.io.Serializable;
import java.util.List;
import lombok.Data;

@Data
public class PromoMessageDto implements Serializable {
  private static final long serialVersionUID = 1L;
  private String action;
  private String promotionId;
  private String brand;
  private String startDate;
  private String endDate;
  private List<LeaderboardConfigDto> promoLbConfigs;
}
