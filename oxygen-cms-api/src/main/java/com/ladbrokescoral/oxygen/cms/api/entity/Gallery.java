package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "galleries")
@Data
@EqualsAndHashCode(callSuper = true)
public class Gallery extends AbstractEntity {
  private String key;
  private String name;
  private List<Filename> images;
  private Instant publishedDate;
}
