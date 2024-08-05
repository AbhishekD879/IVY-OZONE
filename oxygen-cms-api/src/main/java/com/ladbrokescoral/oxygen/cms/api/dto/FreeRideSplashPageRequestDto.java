package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

@Data
@SuppressWarnings("java:S1820")
public class FreeRideSplashPageRequestDto {
  private String id;

  @NotBlank private String brand;
  @NotBlank private String welcomeMsg;
  @NotBlank private String buttonText;
  private String termsAndCondition;
  private String termsAndConditionLink;
  private String termsAndConditionHyperLinkText;

  private MultipartFile splashImg;
  private MultipartFile bannerImg;
  private MultipartFile freeRideLogoImg;

  private Filename splashImage;
  private String splashImageName;
  private Filename bannerImage;
  private String bannerImageFileName;
  private Filename freeRideLogo;
  private String freeRideLogoFileName;

  private Boolean isHomePage;
  private Boolean isBetReceipt;
  private String promoUrl;

  private String createdBy;
  private String createdByUserName;
  private String updatedBy;
  private String updatedByUserName;
  private Instant createdAt;
  private Instant updatedAt;
}
