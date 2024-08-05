package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class MarketLinkData extends AbstractEntity implements HasBrand {
  @Brand private String brand;
  private boolean enabled;

  @NotBlank
  @JsonView(Views.Public.class)
  private String marketName;

  @NotBlank
  @JsonView(Views.Public.class)
  private String linkName;

  @NotBlank
  @JsonView(Views.Public.class)
  private String tabKey;

  @NotBlank
  @JsonView(Views.Public.class)
  private String overlayKey;
}
