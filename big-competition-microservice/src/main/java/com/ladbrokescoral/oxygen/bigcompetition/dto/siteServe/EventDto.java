package com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe;

import com.ladbrokescoral.oxygen.bigcompetition.dto.ParticipantDto;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class EventDto {
  private String id;
  private String name;
  private String eventStatusCode;
  private Boolean isActive;
  private Boolean isDisplayed;
  private Integer displayOrder;
  private String siteChannels;
  private String eventSortCode;
  private String startTime;
  private String rawIsOffCode;
  private String classId;
  private String typeId;
  private String sportId;
  private String liveServChannels;
  private String liveServChildrenChannels;
  private String categoryId;
  private String categoryCode;
  private String categoryName;
  private String className;
  private Integer classDisplayOrder;
  private Integer typeDisplayOrder;
  private String typeName;
  private String typeFlagCodes;
  private String cashoutAvail;
  public String responseCreationTime;
  public Integer marketsCount;
  private String eventFlagCodes;
  public Map<String, ParticipantDto> participants = new HashMap<>();
  private List<MarketDto> markets = new ArrayList<>();
}
