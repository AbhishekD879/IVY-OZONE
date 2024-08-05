package com.ladbrokescoral.oxygen.cms.api.entity.freeride;

import java.util.List;
import lombok.Data;

@Data
public class EventClassInfo {
  private Integer categoryId;
  private Integer classId;
  private List<MarketPlace> marketPlace;
}
