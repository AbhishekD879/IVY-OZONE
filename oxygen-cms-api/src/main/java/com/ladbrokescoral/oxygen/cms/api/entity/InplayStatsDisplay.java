package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "inplay-stats-display")
@Data
@EqualsAndHashCode(callSuper = true)
public class InplayStatsDisplay extends SortableEntity implements HasBrand {

  private String brand;

  private Integer categoryId;

  private String label;

  private String statsKey;
}
