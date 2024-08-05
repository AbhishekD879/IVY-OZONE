package com.ladbrokescoral.oxygen.cms.api.dto;

import java.time.Instant;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.annotation.Id;

@Data
@EqualsAndHashCode(callSuper = true)
public class NavigationPointSegmentedDto extends AbstractSegmentDto {
  @Id private String id;
  private List<Integer> categoryId;
  private List<String> competitionId;
  private List<String> homeTabs;
  private boolean enabled;
  private String targetUri;
  private String title;
  private String description;
  private Instant validityPeriodEnd;
  private Instant validityPeriodStart;
  private String brand;
  private Double sortOrder;
  private String ctaAlignment;
  private String shortDescription;
  private String themes;
  private String bgImageUrl;
}
