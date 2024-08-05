package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractSegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "homeInplaySport")
@EqualsAndHashCode(callSuper = true)
@AllArgsConstructor
@NoArgsConstructor
@Builder
public class HomeInplaySport extends AbstractSegmentEntity {

  private int eventCount;
  private String categoryId;
  private String tier;
  private String sportName;
  private int sportNumber;
  @Brand protected String brand;
}
