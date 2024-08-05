package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class StatsSortingDto {

  private boolean showStatsSorting;

  private Integer reorderDisplayIn;

  private List<InplayStatsSortingDto> statsSortingDtoList = new ArrayList<>();
}
