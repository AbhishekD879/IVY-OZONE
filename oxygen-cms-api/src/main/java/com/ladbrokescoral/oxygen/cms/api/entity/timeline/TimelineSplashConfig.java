package com.ladbrokescoral.oxygen.cms.api.entity.timeline;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "timelineSplashConfig")
@CompoundIndex(
    name = "brand_sorting_fields",
    def = "{'brand' : 1, 'name': 1, 'updatedByUserName': 1, 'updatedAt': 1 }")
@Data
@EqualsAndHashCode(callSuper = true)
public class TimelineSplashConfig extends AbstractTimelineEntity<TimelineSplashConfig>
    implements HasBrand, Auditable<TimelineSplashConfig> {
  @NotBlank private String brand;

  private boolean showSplashPage;
  private String text;

  private String updatedByUserName;
  private String createdByUserName;

  @Override
  public TimelineSplashConfig content() {
    return this;
  }
}
