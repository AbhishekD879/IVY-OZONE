package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.experimental.Accessors;

@Data
@NoArgsConstructor
@Accessors(chain = true)
public class VirtualSportDto {
  private String id;
  private String title;
  private List<VirtualSportTrackDto> tracks;
  private String svgId;
  private String svg;
  private String ctaButtonUrl;
  private String ctaButtonText;

  private String sportsName;
  private String desktopImageId;
  private String mobileImageId;
  private String redirectionURL;
  private String signposting;
  private boolean isTopSports;
  private int topSportsIndex;
}
