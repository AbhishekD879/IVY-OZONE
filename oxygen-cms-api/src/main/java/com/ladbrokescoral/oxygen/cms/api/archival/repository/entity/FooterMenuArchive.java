package com.ladbrokescoral.oxygen.cms.api.archival.repository.entity;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import java.time.Instant;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.CreatedDate;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "footerMenuArchive")
@Data
@NoArgsConstructor
public class FooterMenuArchive extends FooterMenu {

  @CreatedDate
  @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX",
      timezone = "UTC")
  private Instant archivalDate;

  private boolean deleted;
}