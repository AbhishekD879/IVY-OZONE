package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidSvgSprite;
import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class SvgImageDto {
  @NotBlank @Brand private String brand;
  private boolean active;
  private String svgId;
  @ValidSvgSprite private String sprite;
  private String description;
  private String svg;
}
