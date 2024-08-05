package com.coral.oxygen.middleware.pojos.model.cms;

import java.util.List;
import java.util.Map;
import lombok.Data;

/** Created by azayats on 25.01.17. */
@Data
public class CmsInplayData {
  private List<SportItem> activeSportCategories;
  private Map<String, SportItem> sportMap;
  private List<VirtualSportDto> virtualSports;
}
