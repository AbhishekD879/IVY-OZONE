package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class SportsFeaturedTabDto {
  private String name;
  private String categoryId;
  private List<SimpleModuleDto> modules;
}
