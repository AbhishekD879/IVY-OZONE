package com.ladbrokescoral.oxygen.cms.api.entity.freeride;

import java.util.List;
import lombok.Data;

@Data
public class MarketPlace {
  private String typeId;
  private String typeName;
  private List<Event> events;
}
