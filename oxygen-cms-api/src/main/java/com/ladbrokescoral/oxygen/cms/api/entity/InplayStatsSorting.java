package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "inplay-stats-sorting")
@EqualsAndHashCode(callSuper = true)
public class InplayStatsSorting extends SortableEntity implements HasBrand {

  private String brand;

  private Integer categoryId;

  private String label;

  private String referenceKey;

  private boolean enabled;
}
