package com.coral.oxygen.middleware.pojos.model.cms;

import lombok.Data;

/**
 * This FanzoneConfiguration class is for holding fanzone configuration details which are getting
 * from Oxygen-cms-api. This FanzoneConfiguration details help for enable entry points for Fanzone
 * Page and Enable/Disable Fanzone tabs .
 */
@Data
// @JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
public class FanzoneConfiguration {
  private Boolean showCompetitionTable;
  private Boolean showNowNext;
  private Boolean showStats;
  private Boolean showClubs;
  private Boolean sportsRibbon;
  private Boolean homePage;
  private Boolean footballHome;
  private Boolean atozMenu;
}
