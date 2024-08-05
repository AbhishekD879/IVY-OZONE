package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class LuckyDipFieldsConfig extends LuckyDipFieldsConfigV2 {
  @NotBlank private String desc;
}
