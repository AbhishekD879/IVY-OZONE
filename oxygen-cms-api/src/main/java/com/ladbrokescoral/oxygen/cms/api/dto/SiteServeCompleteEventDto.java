package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SiteServeCompleteEventDto {
  private Long id;
  private String name;
  private String eventSortCode;
  private String startTime;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String liveServLastMsgId;
  private String categoryId;
  private String categoryCode;
  private String categoryName;
  private String classId;
  private String className;
  private String typeId;
  private String typeName;
  private String cashoutAvail;
  private String eventStatusCode;

  private Boolean eventIsLive;
  private Integer displayOrder;

  private List<SiteServeCompleteMarketDto> markets;

  private Boolean isStarted;
  private Boolean isFinished;

  private String responseCreationTime;
  protected String drilldownTagNames;
  private String typeFlagCodes;
  private String eventFlagCodes;
}
