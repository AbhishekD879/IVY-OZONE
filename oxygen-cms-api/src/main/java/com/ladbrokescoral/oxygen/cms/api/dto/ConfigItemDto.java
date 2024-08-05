package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;
import org.springframework.data.annotation.Id;

@Data
public class ConfigItemDto {
  @Id private String id;
  private String name;
  private boolean overwrite;
  private boolean initialDataConfig = true;
  private List<ConfigItemPropertyDto> items;
}
