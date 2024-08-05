package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class BottomMenuDto extends BaseMenuDto {
  private Boolean authRequired;
  private Integer systemID;
  private String startUrl;
}
