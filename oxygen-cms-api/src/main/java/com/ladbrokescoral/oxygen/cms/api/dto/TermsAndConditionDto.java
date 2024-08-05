package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.validation.annotation.Validated;

@Data
@Validated
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class TermsAndConditionDto extends SortableEntity implements HasBrand {
  @NotNull private String text;
  @NotNull private String brand;
  private String title;
  private String url;
}
