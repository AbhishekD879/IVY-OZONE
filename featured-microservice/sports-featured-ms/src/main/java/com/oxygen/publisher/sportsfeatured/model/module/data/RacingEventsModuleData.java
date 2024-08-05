package com.oxygen.publisher.sportsfeatured.model.module.data;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class RacingEventsModuleData extends AbstractModuleData {
  private String id;
  private String name;
  private String categoryId;
  private String categoryName;
  private String classId;
  private String className;
  private String typeName;
  private String startTime;
  private String cashoutAvail;
  private Integer displayOrder;
  private Integer classDisplayOrder;
  private Integer typeDisplayOrder;
  private Boolean isStarted;
  private Boolean isLiveNowEvent;
  private Boolean isFinished;
  private Boolean isResulted;
  private String rawIsOffCode;
  private String typeFlagCodes;
  private String drilldownTagNames;
  private List<String> poolTypes;
  private List<RacingEventMarket> markets;
  private String effectiveGpStartTime;
  private String eventStatusCode;
  private String liveServChannels;
  private String liveServChildrenChannels;
}
