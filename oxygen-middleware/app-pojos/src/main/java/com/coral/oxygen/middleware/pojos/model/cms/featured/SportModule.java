package com.coral.oxygen.middleware.pojos.model.cms.featured;

import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import com.coral.oxygen.middleware.pojos.model.output.featured.ModuleType;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import javax.validation.constraints.NotEmpty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import lombok.ToString;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
@ToString
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class SportModule {

  private PageType pageType;
  private String id;
  private Integer sportId;
  private Double sortOrder;
  private boolean segmented;
  private String pageId;

  @NotEmpty private String title;

  protected String brand;

  private ModuleType moduleType;

  private List<String> publishedDevices;

  public BigDecimal getSortOrderOrDefault(BigDecimal defaultIfNull) {
    return Optional.ofNullable(sortOrder).map(BigDecimal::new).orElse(defaultIfNull);
  }
}
