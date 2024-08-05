package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class CountrySettingDto {
  private String val;
  private String phoneAreaCode;
  private String label;
}
