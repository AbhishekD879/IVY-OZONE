package com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe;

import com.ladbrokescoral.oxygen.bigcompetition.dto.ParticipantDto;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import lombok.Data;

@Data
public class OutcomeDto {

  private String id;
  private String marketId;
  private String name;
  private String outcomeMeaningMajorCode;
  private String outcomeMeaningMinorCode;
  private Boolean isDisplayed;
  private Integer displayOrder;
  private String outcomeStatusCode;
  private String liveServChannels;
  private String cashoutAvail;
  private boolean hasPriceStream;
  private List<PriceDto> prices = new ArrayList<>();
  private Map<String, ParticipantDto> participants = new HashMap<>();
}
