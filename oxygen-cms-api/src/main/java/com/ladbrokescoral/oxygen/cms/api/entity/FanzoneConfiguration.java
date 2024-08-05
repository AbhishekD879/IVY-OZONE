package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;

@Data
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class FanzoneConfiguration {
  private Boolean showCompetitionTable;
  private Boolean showNowNext;
  private Boolean showStats;
  private Boolean showClubs;
  private Boolean sportsRibbon;
  private Boolean homePage;
  private Boolean footballHome;
  private Boolean atozMenu;
  private String fanzoneBannerDesktop;
  private String launchBannerUrlDesktop;
  private Boolean showGames = false;
  private Boolean showSlotRivals = false;
  private Boolean showScratchCards = false;
  private Boolean showBetsBasedOnYourTeam = false;
  private Boolean showBetsBasedOnOtherFans = false;
}
