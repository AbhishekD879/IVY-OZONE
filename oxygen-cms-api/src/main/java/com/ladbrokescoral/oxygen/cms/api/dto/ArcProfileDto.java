package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.SportsAction;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.NonNull;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class ArcProfileDto extends SortableEntity implements HasBrand {

  @NonNull private String profile;
  @NonNull private String modelRiskLevel;
  @NonNull private String reasonCode;
  @NonNull private List<SportsAction> sportsActions;
  @NonNull private String frequency;
  @NonNull private Boolean enabled;
  @NonNull private String brand;
}
