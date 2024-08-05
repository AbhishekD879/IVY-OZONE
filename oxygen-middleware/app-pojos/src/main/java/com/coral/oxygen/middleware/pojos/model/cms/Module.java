package com.coral.oxygen.middleware.pojos.model.cms;

import com.coral.oxygen.middleware.pojos.model.cms.featured.AbstractSegment;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import java.io.Serializable;
import java.math.BigDecimal;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class Module extends AbstractSegment implements Serializable {
  private String _id; // 5818a0b843fefc07006d1435",
  private String title; // "Test Sports",
  private BigDecimal displayOrder; // 0,
  private Boolean showExpanded; // false,
  private String navItem; // "Featured",
  private Integer maxRows; // 5,
  private String maxSelections; // 5,
  private Integer totalEvents; // 36,
  private List<String> publishedDevices; // ": ["desktop", "tablet", "mobile"],
  private Integer __v; // 1,
  private List<EventsModuleData> data; // [],
  private ModuleDataSelection dataSelection; // {"selectionType": "Type","selectionId": "435"},
  private Map<String, String> footerLink; // {"text": "","url": ""},
  private List<String>
      publishToChannels; // ["bma","gf","secondscreen","partner","rcomb","retail","connect"],
  private Map<String, String> eventsSelectionSettings; // {"from": "2016-10-30T22:00:00.000Z","to":
  // "2016-11-04T21:59:00.000Z"},
  private Boolean shouldBeDisplayed; // false,
  private Boolean cashoutAvail; // false
  private String badge;
  private boolean groupedBySport;
}
