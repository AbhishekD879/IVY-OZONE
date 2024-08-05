package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class TopMenuDto {
  private String linkTitle;
  private String targetUri;
  private Boolean disabled;
}
