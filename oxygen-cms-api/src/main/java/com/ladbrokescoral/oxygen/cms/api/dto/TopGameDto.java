package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class TopGameDto extends BaseUIDto {
  private Integer widthSmallIcon;
  private Integer widthMediumIcon;
  private Integer widthLargeIcon;
  private Integer heightSmallIcon;
  private Integer heightMediumIcon;
  private Integer heightLargeIcon;
  private String imageTitle;
  private String path;
  private String targetUri;
  private Boolean disabled;
  private String alt;
  private String showItemOn;
}
