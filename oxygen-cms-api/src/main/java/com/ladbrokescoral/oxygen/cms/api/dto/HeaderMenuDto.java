package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class HeaderMenuDto extends BaseMenuDto {
  private List<BaseMenuDto> children;
}
