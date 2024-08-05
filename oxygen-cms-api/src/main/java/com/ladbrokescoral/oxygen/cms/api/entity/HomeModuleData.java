package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Field;

@Data
public class HomeModuleData {

  @Field("id")
  private String id;

  private String categoryId;
  private String nameOverride;
  private String name;
  private Boolean outright;
  private String marketCount;
}
