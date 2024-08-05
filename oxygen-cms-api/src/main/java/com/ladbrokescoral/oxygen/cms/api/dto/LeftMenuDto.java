package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class LeftMenuDto {
  private String targetUri;
  private String linkTitle;
  private Boolean inApp;
  private String showItemFor;
  private List<Object> children;
}
