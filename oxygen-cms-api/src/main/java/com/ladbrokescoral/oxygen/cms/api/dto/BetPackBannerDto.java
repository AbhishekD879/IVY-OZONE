package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import java.time.Instant;
import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

@Data
public class BetPackBannerDto {
  private String id;

  @NotNull private String welcomeMsg;

  @NotNull private String brand;
  @NotNull private String termsAndCondition;
  @NotNull private String termsAndConditionLink;
  private MultipartFile bannerImg;
  @NotNull private boolean enabled;
  private Filename bannerImage;
  private String bannerImageFileName;
  private String createdBy;
  private String createdByUserName;
  private String updatedBy;
  private String updatedByUserName;
  private Instant createdAt;
  private Instant updatedAt;

  // OZONE-5901
  // Expiring Bet Bundle Token(s) Banners
  @NotNull private boolean bannerActiveInMarketPlace;
  private String marketPlaceImageFileName;
  private String marketPlaceBgImageFileName;
  private String bannerTextDescInMarketPlacePage;

  @NotNull private boolean bannerActiveInReviewPage;
  private String reviewPageImageFileName;
  private String reviewPageBgImageFileName;
  private String bannerTextDescInReviewPage;

  @NotNull private boolean expiresInActive;
  private String expiresInText;

  private String expiresInIconImage;
}
