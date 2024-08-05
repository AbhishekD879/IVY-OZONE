package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import lombok.Data;

@Data
public class CompetitionSpecialModuleData {

  private List<Integer> typeIds;
  private List<Integer> eventIds;
  private String linkUrl;
}
