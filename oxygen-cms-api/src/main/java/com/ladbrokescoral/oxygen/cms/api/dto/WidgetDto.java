package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import lombok.Data;

@Data
public class WidgetDto {
  private String title;
  private String directiveName;
  private Boolean showExpanded;
  private List<String> publishedDevices;
  private List<String> columns;

  @JsonInclude(JsonInclude.Include.NON_NULL)
  private ShowOnDto showOn;
}
