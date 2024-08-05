package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.annotation.Id;

@Data
@EqualsAndHashCode(callSuper = true)
public class RacingEdpMarketDto extends SortableEntity {

  @JsonView(Views.Public.class)
  @Id
  private String id;

  @JsonView(Views.Public.class)
  @NotBlank
  private String name;

  @JsonView(Views.Public.class)
  @NotBlank
  private String brand;

  @JsonView(Views.Public.class)
  @NotNull
  private String description;

  @JsonView(Views.Public.class)
  private String birDescription;

  @JsonView(Views.Public.class)
  @JsonProperty("isHR")
  private boolean hr;

  @JsonView(Views.Public.class)
  @JsonProperty("isGH")
  private boolean gh;

  @JsonView(Views.Public.class)
  @JsonProperty("isNew")
  private boolean label;
}
