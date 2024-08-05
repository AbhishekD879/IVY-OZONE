package com.ladbrokescoral.oxygen.cms.api.entity;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;

@Data
public class CountryData {

  @NotBlank private String val;
  @NotBlank private String phoneAreaCode;
  @NotBlank private String label;
  @NotNull private Boolean allowed;
}
