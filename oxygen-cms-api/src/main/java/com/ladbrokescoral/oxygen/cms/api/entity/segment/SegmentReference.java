package com.ladbrokescoral.oxygen.cms.api.entity.segment;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import lombok.experimental.SuperBuilder;
import org.springframework.data.mongodb.core.index.Indexed;

@Data
@SuperBuilder
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class SegmentReference extends AbstractEntity {

  private String pageRefId;
  @NonNull @Indexed private String segmentName;
  private Double sortOrder;

  public void updateSortOrder(Double sortOrder) {
    this.sortOrder = sortOrder;
    this.setUpdatedAt(Instant.now());
  }
}
