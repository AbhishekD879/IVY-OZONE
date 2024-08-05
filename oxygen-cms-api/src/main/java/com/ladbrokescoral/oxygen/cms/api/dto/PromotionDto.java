package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPack;
import com.ladbrokescoral.oxygen.cms.api.entity.PromoFreeRideConfig;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.ToString;

@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = true)
@ToString(callSuper = true)
public class PromotionDto extends PromotionV2Dto {

  @JsonProperty("requestId")
  private String requestId = "";

  private List<String> categoryId;

  private BetPack betPack;

  private PromoFreeRideConfig freeRideConfig;

  private String id;
}
