package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class SimpleModuleDto {
  private String originalName;
  private String displayName;
  private String description;
  private Integer displayOrder;
}
