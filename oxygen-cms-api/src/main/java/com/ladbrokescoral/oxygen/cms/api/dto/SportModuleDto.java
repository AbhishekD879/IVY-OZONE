package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import java.util.List;
import lombok.Data;

@Data
public class SportModuleDto {
  private String id;
  private Integer sportId;
  private String pageId;
  private PageType pageType;
  private SportModuleType moduleType;
  private String title;
  private String brand;
  private List<String> publishedDevices;
  private Double sortOrder;

  @JsonIgnore
  public SportGroupKey getGroupKey() {
    return new SportGroupKey(pageId, pageType);
  }
}
