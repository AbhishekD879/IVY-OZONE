package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.entity.timeline.AbstractTimelineEntity;
import javax.validation.constraints.NotNull;
import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "fanzones")
public class FanzonePage extends AbstractTimelineEntity<FanzonePage> implements HasBrand {
  @NotNull private String pageName;
  @NotNull private String brand;
}
