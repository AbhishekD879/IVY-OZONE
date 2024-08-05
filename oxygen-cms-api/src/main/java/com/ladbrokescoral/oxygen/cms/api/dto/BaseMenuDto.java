package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class BaseMenuDto {
  @Id private String id;
  private String linkTitle;
  private String targetUri;
  private Boolean disabled;
  private Boolean inApp;
}
