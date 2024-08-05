package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import com.ladbrokescoral.oxygen.cms.api.entity.MarketType;
import com.ladbrokescoral.oxygen.cms.api.entity.SortableEntity;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "statisticalContent")
@CompoundIndex(name = "statistical_contents", def = "{'eventId' : 1, 'marketId' : 1, 'brand' : 1}")
@Data
@EqualsAndHashCode(callSuper = true)
public class StatisticContent extends SortableEntity implements HasBrand {

  private String brand;

  private String title;

  private MarketType marketType;

  private String marketDescription;

  private String eventId;

  private String marketId;

  private String content;

  private boolean enabled;

  private Instant startTime;

  private Instant endTime;
}
