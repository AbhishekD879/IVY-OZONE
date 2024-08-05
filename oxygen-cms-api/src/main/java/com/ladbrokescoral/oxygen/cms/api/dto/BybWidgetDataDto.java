package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class BybWidgetDataDto extends AbstractDto {

  @NotBlank private String title;
  @NotBlank private String eventId;
  @NotBlank private String marketId;
  @NotNull private Instant displayFrom;
  @NotNull private Instant displayTo;
  private Double sortOrder;

  @NotEmpty private List<String> locations;
}
