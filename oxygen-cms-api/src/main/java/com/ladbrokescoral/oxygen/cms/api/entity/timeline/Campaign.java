package com.ladbrokescoral.oxygen.cms.api.entity.timeline;

import static com.ladbrokescoral.oxygen.cms.api.entity.timeline.CampaignStatus.CLOSED;
import static com.ladbrokescoral.oxygen.cms.api.entity.timeline.CampaignStatus.OPEN;

import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Positive;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "timelineCampaign")
@CompoundIndex(
    name = "brand_sorting_fields",
    def =
        "{'brand' : 1, 'name': 1, 'status': 1, 'displayFrom': 1, 'displayTo': 1, 'updatedByUserName': 1, 'updatedAt': 1 }")
@Data
@EqualsAndHashCode(callSuper = true)
@DateRange(startDateField = "displayFrom", endDateField = "displayTo")
@Slf4j
public class Campaign extends AbstractTimelineEntity<Campaign>
    implements HasBrand, Auditable<Campaign> {
  @NotBlank private String brand;
  @NotBlank private String name;

  @Positive private int messagesToDisplayCount;

  private Instant displayFrom;
  private Instant displayTo;

  @NotNull private CampaignStatus status;
  private List<String> postsIds;

  private String updatedByUserName;
  private String createdByUserName;

  public boolean isDisplayed() {
    return status == CampaignStatus.LIVE
        && displayFrom.isBefore(Instant.now())
        && displayTo.isAfter(Instant.now());
  }

  public boolean isScheduled() {
    return status == CampaignStatus.LIVE && displayTo.isAfter(Instant.now());
  }

  public boolean isExpired() {
    return getDisplayTo().isBefore(Instant.now())
        || getStatus() == CLOSED
        || getStatus().equals(OPEN);
  }

  @Override
  public Campaign content() {
    return this;
  }
}
