package com.coral.oxygen.middleware.ms.quickbet.connector.dto.response;

import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;

/** Created by azayats on 24.10.17. */
@Data
@NoArgsConstructor
public final class OutputEvent {
  private String id;
  private String name;
  private List<OutputMarket> markets;
  private String eventStatusCode;
  private Boolean isLiveNowEvent = false;
  private Boolean isStarted = false;
  private String startTime;
  private String typeId;
  private String typeName;
  private String categoryId;
  private String categoryName;
  private String classId;
  private String className;
  private String drilldownTagNames;
  private String isCashoutAvailable;
  private String eventFlagCodes;
}
