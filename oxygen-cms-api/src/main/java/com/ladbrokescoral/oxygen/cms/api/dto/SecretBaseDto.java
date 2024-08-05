package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidURI;
import javax.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class SecretBaseDto {
  private String id;
  @Brand @NotBlank private String brand;
  @ValidURI private String uri;
  @NotBlank private String name;
  private boolean enabled;
}
