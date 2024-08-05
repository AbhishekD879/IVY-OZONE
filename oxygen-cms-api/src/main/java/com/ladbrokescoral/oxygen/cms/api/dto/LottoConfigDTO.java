package com.ladbrokescoral.oxygen.cms.api.dto;

import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class LottoConfigDTO extends AbstractDto {

  private String SsMappingId;
  @NotNull private String label;
  private String infoMessage;
  private String nextLink;
  private Double sortOrder;
  private String bannerLink;
  private String svgId;
  private String bannerText;
  private boolean isEnabled;
  private Integer dayCount;
  private Double maxPayOut;
}
