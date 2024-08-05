package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class FooterMenuV2Dto {
  @Id private String id;
  private String targetUri;
  private String linkTitle;
  private String uriSmall;
  private String uriMedium;
  private String uriLarge;
  private Boolean inApp;
  private String showItemFor;
  private Boolean disabled;
  private String svg;
  private String svgId;
  private Boolean authRequired;
  private Integer systemID;
}
