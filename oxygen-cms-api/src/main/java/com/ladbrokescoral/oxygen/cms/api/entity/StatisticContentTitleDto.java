package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import lombok.Data;

@Data
public class StatisticContentTitleDto {

  private String eventTitle;

  private List<String> marketIds;
}
