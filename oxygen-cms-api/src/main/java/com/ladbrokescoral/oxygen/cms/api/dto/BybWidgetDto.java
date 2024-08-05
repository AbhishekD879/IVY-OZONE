package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class BybWidgetDto extends AbstractDto {

  @NotBlank private String title;
  private int marketCardVisibleSelections;
  private boolean showAll;
  private List<BybWidgetDataDto> data = new ArrayList<>();
  private Map<String, Boolean> displayOn = new HashMap<>();
}
