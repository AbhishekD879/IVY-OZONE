package com.ladbrokescoral.oxygen.seo.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.*;

@Data
@NoArgsConstructor
@AllArgsConstructor
@EqualsAndHashCode(callSuper = true)
@ToString(callSuper = true)
public class PromotionDto extends PromotionV2Dto {

  @JsonProperty("requestId")
  private String requestId = "";

  private List<String> categoryId;
}
