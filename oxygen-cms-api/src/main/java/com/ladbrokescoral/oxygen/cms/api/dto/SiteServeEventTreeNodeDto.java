package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class SiteServeEventTreeNodeDto {
  private String id;
  private String name;

  private String typeId;
  private String typeName;

  private String classId;
  private String className;

  private String categoryId;
  private String categoryName;
}
