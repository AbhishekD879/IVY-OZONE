package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "otf-ios-app-toggle")
public class OtfIosAppToggle extends AbstractEntity implements HasBrand {

  @Brand private String brand;

  @NotBlank private String text;

  private boolean iosAppOff;
  private String url;
  private String urlText;

  @NotBlank private String closeCtaText;

  private String proceedCtaText;
}
