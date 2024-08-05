package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
public class HeaderContactMenuDto {
  private String id;
  private Boolean authRequired;
  private Boolean disabled;
  private Boolean inApp;
  private Integer systemID;
  private String linkTitle;
  private String label;
  private String targetUri;

  @JsonInclude(JsonInclude.Include.NON_EMPTY)
  private String startUrl;
}
