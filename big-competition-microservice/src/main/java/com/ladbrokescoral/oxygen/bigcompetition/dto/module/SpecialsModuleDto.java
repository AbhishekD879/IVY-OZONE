package com.ladbrokescoral.oxygen.bigcompetition.dto.module;

import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import java.util.Set;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class SpecialsModuleDto extends CompetitionModuleDto {
  private Set<EventDto> events;
  private String linkUrl;
}
