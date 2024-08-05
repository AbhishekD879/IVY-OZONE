package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonProperty;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "racingedpmarkets")
@Data
@EqualsAndHashCode(callSuper = true)
public class RacingEdpMarket extends SortableEntity implements HasBrand {
  @NotBlank private String name;
  @NotBlank private String brand;
  @NotNull private String description;
  private String birDescription;

  @JsonProperty("isHR")
  private boolean hr;

  @JsonProperty("isGH")
  private boolean gh;

  @JsonProperty("isNew")
  private boolean label;
}
