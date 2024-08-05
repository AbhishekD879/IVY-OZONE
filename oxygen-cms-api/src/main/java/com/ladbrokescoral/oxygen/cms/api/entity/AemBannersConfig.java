package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@DateRange(startDateField = "displayFrom", endDateField = "displayTo")
public class AemBannersConfig implements SportModuleConfig {

  @NotNull private Integer maxOffers;
  @NotNull private Integer timePerSlide;
  @NotNull private Instant displayFrom;
  @NotNull private Instant displayTo;
}
