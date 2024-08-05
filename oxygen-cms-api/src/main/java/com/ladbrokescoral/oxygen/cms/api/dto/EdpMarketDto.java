package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class EdpMarketDto {
  @Id private String id;
  private String name;
  private String marketId;
  private Boolean lastItem;
}
