package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.Auditable;
import java.util.List;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
@Document(collection = "betpack-onboarding")
@EqualsAndHashCode(callSuper = false)
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class BetPackOnboarding extends SortableEntity
    implements HasBrand, Auditable<BetPackOnboarding> {

  @Indexed(unique = true)
  @NotNull
  private String brand;

  private Boolean isActive;
  private List<OnboardingImage> images;

  private String updatedByUserName;
  private String createdByUserName;

  @Override
  public BetPackOnboarding content() {
    return this;
  }
}
