package com.ladbrokescoral.oxygen.cms.api.entity.freeride;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "freeridesplashpage")
public class FreeRideSplashPage extends AbstractEntity implements HasBrand {
  private String brand;
  private String welcomeMsg;
  private String termsAndCondition;
  private String termsAndConditionLink;
  private String termsAndConditionHyperLinkText;
  private String buttonText;
  private Filename splashImage;
  private String splashImageName;
  private Filename bannerImage;
  private String bannerImageFileName;
  private Filename freeRideLogo;
  private String freeRideLogoFileName;

  private Boolean isHomePage = false;
  private Boolean isBetReceipt = false;

  private String promoUrl;
}
