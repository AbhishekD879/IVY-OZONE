package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import lombok.Data;

@Data
public class NavigationPointDto {
  private List<Integer> categoryId; // List of sport category IDs to show quick link on
  private List<String> competitionId; // List of big competition IDs to show quick link on
  private List<String> competitionTabs;
  private List<String> homeTabs; // List of module ribbon tabs URLs to show quick link on
  private String targetUri;
  private String title;
  private String description;
  private Instant validityPeriodEnd;
  private Instant validityPeriodStart;
  private String ctaAlignment;
  private String shortDescription;
  private String themes;
  private String bgImageUrl;
}
