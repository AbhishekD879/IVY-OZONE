package com.ladbrokescoral.oxygen.cms.api.dto;

import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class SeoAutoInitDataDto {
  @NotBlank private String metaTitle;
  @NotBlank private String metaDescription;
}
