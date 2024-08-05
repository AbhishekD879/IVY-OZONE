package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.validation.annotation.Validated;

@Data
@Validated
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class TermsAndCondition extends SortableEntity implements HasBrand {
  @NotNull private String text;
  @NotNull private String brand;
  @NotNull private String title;
  @NotNull private String url;
}
