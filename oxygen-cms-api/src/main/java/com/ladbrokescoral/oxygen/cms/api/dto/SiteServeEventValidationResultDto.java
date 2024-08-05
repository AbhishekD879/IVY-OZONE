package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class SiteServeEventValidationResultDto {
  private List<SiteServeMinimalEventDto> valid; // list of events with valid ids
  private List<String> invalid; // list of invalid event ids
}
