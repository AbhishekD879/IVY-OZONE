package com.ladbrokescoral.oxygen.cms.api.service.siteserve;

import com.ladbrokescoral.oxygen.cms.api.entity.TypeFlagCodes;
import java.util.Comparator;
import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class NextEventsParameters {

  private String brand;
  private int categoryId;
  private TypeFlagCodes typeFlagCodes;
  private Comparator comparator;
  private int timePeriodMinutes;
}
