package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzones")
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@EqualsAndHashCode(callSuper = true)
public class Fanzone extends FanzonePage {
  @NotBlank private String name;
  @NotBlank private String teamId;
  private String openBetID;
  private String assetManagementLink;
  private String launchBannerUrl;
  private String fanzoneBanner;

  @Pattern(regexp = Patterns.COMMA_SEPARTED_NUMBERS, message = "must be valid comma separated ids")
  private String primaryCompetitionId;

  @Pattern(regexp = Patterns.COMMA_SEPARTED_NUMBERS, message = "must be valid comma separated ids")
  private String secondaryCompetitionId;

  @Pattern(regexp = Patterns.COMMA_SEPARTED_NUMBERS, message = "must be valid comma separated ids")
  private String clubIds;

  private String hexColorCode;

  private String location;
  private String nextGamesLbl;
  private String outRightsLbl;
  private String premierLeagueLbl;
  private Boolean active;
  private String updatedByUserName;
  private String createdByUserName;
  private FanzoneConfiguration fanzoneConfiguration;
  private Boolean is21stOrUnlistedFanzoneTeam;
}
