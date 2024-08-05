package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "games")
@Data
@EqualsAndHashCode(callSuper = true)
@DateRange(startDateField = "displayFrom", endDateField = "displayTo")
public class Game extends AbstractEntity implements HasBrand {

  @Brand private String brand;

  @NotBlank private String title;

  @NotNull private Instant displayFrom;

  @NotNull private Instant displayTo;

  private boolean enabled;

  private List<Prize> prizes;
  private List<GameEvent> events;
  private String seasonId;
}
