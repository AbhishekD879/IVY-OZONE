package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class BaseUIDto {
  @Id private String id;
  private String filename;
  private String uriMedium;
  private String uriLarge;
  private String uriSmall;
  private Integer widthLarge;
  private Integer widthMedium;
  private Integer widthSmall;
  private Integer heightLarge;
  private Integer heightMedium;
  private Integer heightSmall;
  private String uriLargeIcon;
  private String uriMediumIcon;
  private String uriSmallIcon;
}
