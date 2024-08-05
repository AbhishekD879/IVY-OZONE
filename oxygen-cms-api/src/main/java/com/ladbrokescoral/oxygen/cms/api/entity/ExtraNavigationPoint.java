package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "extraNavigationPoint")
public class ExtraNavigationPoint extends SortableEntity implements HasBrand {

  private List<Integer> categoryId; // List of sport category IDs to show quick link on
  private List<String> competitionId; // List of big competition IDs to show quick link on
  private List<String> competitionTabs;
  private List<String> homeTabs; // List of module ribbon tabs URLs to show quick link on
  private boolean enabled;
  @NotBlank private String targetUri;

  @NotBlank
  @Size(max = 25, min = 1)
  private String title;

  @Size(max = 45)
  private String description;

  @NotNull private Instant validityPeriodEnd;
  @NotNull private Instant validityPeriodStart;
  @Brand protected String brand;

  @NotNull private String featureTag;
  private String bgImageUrl;

  @Size(max = 65)
  private String shortDescription;

  private boolean isBgAlignmentEnabled;
}
