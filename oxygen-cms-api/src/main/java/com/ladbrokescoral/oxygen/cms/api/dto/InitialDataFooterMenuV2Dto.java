package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class InitialDataFooterMenuV2Dto {
  private String id;
  private String targetUri;
  private String linkTitle;
  private Boolean inApp;
  private String showItemFor;
  private Boolean disabled;
  private String svgId;
}
