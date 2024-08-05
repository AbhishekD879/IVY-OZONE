package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "bybWidgetData")
@EqualsAndHashCode(callSuper = true)
public class BybWidgetData extends SortableEntity implements HasBrand {

  @Brand public String brand;

  private String title;
  private String eventId;
  private String marketId;
  @NotNull private Instant displayFrom;
  @NotNull private Instant displayTo;

  private List<String> locations;
}
