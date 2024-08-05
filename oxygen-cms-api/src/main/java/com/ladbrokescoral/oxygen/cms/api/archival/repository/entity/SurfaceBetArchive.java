package com.ladbrokescoral.oxygen.cms.api.archival.repository.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document("surfacebetArchive")
@EqualsAndHashCode(callSuper = true)
@DateRange(startDateField = "displayFrom", endDateField = "displayTo")
public class SurfaceBetArchive extends SurfaceBet {
  @CreatedDate
  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant archivalDate;

  private boolean deleted;
}
