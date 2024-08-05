package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class ConnectMenuDto {
  private String svg;
  private String svgId;
  private String targetUri;
  private String linkTitle;
  private String linkSubtitle;
  private Boolean inApp;
  private String showItemFor;
  private List<Object> children;
  private Boolean upgradePopup;
}
