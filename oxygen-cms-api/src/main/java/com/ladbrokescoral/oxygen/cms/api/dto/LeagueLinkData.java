package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class LeagueLinkData extends AbstractEntity implements HasBrand {
  @Brand private String brand;
  private boolean enabled;

  @NotEmpty private List<Integer> couponIds;

  @JsonView(Views.Public.class)
  private int obLeagueId;

  @JsonView(Views.Public.class)
  private int dhLeagueId;

  @NotBlank
  @JsonView(Views.Public.class)
  private String linkName;
}
