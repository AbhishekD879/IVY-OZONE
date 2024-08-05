package com.gvc.oxygen.betreceipts.service.siteserve;

import com.egalacoral.spark.siteserver.model.Event;
import com.gvc.oxygen.betreceipts.entity.TypeFlagCodes;
import java.util.Comparator;
import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class NextEventsParameters {

  private int categoryId;
  private TypeFlagCodes typeFlagCodes;
  private Comparator<Event> comparator;
  private int timePeriodMinutes;
}
