package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class AemBannersDto implements SportPageModuleDataItem {

  private SportPageId sportPageId;
  private String title;
  private Integer maxOffers;
  private Integer timePerSlide;
  private Instant displayFrom;
  private Instant displayTo;

  @Override
  public SportPageId sportPageId() {
    return sportPageId;
  }
}
