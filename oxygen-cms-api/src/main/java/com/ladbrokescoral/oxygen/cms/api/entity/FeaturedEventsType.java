package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "featuredeventstypes")
@Data
@EqualsAndHashCode(callSuper = true)
public class FeaturedEventsType extends AbstractEntity {
  private Integer rowsNum;
  private Integer typeId;
  private String name;
  private Boolean collapsed;
  private Boolean disabled;
  private Instant validityPeriodEnd;
  private Instant validityPeriodStart;
  private String sportCategories;
  @NotBlank private String brand;
  private String lang;
}
