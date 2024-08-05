package com.coral.oxygen.middleware.pojos.model.cms;

import javax.validation.constraints.NotBlank;
import lombok.Data;

/**
 * This Fanzone class is for holding fanzone configuration details which are getting from
 * Oxygen-cms-api. This fanzone details help for validation/filtration for every segments.
 */
@Data
public class Fanzone extends FanzonePage {
  @NotBlank private String name;
  @NotBlank private String teamId;
  private String openBetID;
  private String assetManagementLink;
  private String launchBannerUrl;
  private String fanzoneBanner;
  private String ctaBtnText;
  private String description;

  private String primaryCompetitionId;

  private String secondaryCompetitionId;

  private String clubIds;

  private String location;
  private String nextGamesLbl;
  private String outRightsLbl;
  private String premierLeagueLbl;
  private Boolean active;
  private String updatedByUserName;
  private String createdByUserName;
  private FanzoneConfiguration fanzoneConfiguration;
}
