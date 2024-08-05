package com.ladbrokescoral.oxygen.cms.api.archival.repository.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document("sportCategoryArchive")
@EqualsAndHashCode(callSuper = true)
public class SportCategoryArchive extends SportCategory {
  @CreatedDate
  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant archivalDate;

  private boolean deleted;
}
