package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractSegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class NavigationPoint extends AbstractSegmentEntity {
  @NotNull private String ctaAlignment;

  @Size(max = 65)
  private String shortDescription;

  private String themes;
  private List<Integer> categoryId; // List of sport category IDs to show quick link on
  private List<String> competitionId; // List of big competition IDs to show quick link on
  private List<String> competitionTabs;
  private List<String> homeTabs; // List of module ribbon tabs URLs to show quick link on
  private boolean enabled;
  @NotBlank private String targetUri;

  @NotBlank
  @Size(max = 40, min = 1)
  private String title;

  @Size(max = 65)
  private String description;

  @NotNull private Instant validityPeriodEnd;
  @NotNull private Instant validityPeriodStart;
  @Brand protected String brand;
  private String bgImageUrl;
}
