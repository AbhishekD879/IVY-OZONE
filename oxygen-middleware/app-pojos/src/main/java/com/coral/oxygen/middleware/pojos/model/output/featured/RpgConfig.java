package com.coral.oxygen.middleware.pojos.model.output.featured;

import static org.apache.commons.lang3.StringUtils.*;

import com.coral.oxygen.middleware.pojos.model.cms.featured.RecentlyPlayedGame;
import com.coral.oxygen.middleware.pojos.model.output.AbstractModuleData;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.google.gson.annotations.SerializedName;
import lombok.*;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class RpgConfig extends AbstractModuleData {
  @SerializedName("@type")
  @JsonProperty("@type")
  private String type = "RpgConfig";

  private String title;
  private String seeMoreLink;
  private String bundleUrl;
  private String loaderUrl;
  private Integer gamesAmount;

  public RpgConfig(RecentlyPlayedGame recentlyPlayedGame) {
    this.title = recentlyPlayedGame.getRpgConfig().getTitle();
    this.seeMoreLink = recentlyPlayedGame.getRpgConfig().getSeeMoreLink();
    this.bundleUrl = recentlyPlayedGame.getRpgConfig().getBundleUrl();
    this.loaderUrl = recentlyPlayedGame.getRpgConfig().getLoaderUrl();
    this.gamesAmount = recentlyPlayedGame.getRpgConfig().getGamesAmount();
    this.pageType = recentlyPlayedGame.getPageType();
  }

  @Override
  public String idForChangeDetection() {
    return String.valueOf(
        title.hashCode()
            + seeMoreLink.hashCode()
            + gamesAmount.hashCode()
            + defaultString(bundleUrl).hashCode()
            + defaultString(loaderUrl).hashCode());
  }
}
