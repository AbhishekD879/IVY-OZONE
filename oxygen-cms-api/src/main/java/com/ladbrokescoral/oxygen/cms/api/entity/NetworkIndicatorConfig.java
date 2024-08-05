package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.Data;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "networkIndicator")
@Data
public class NetworkIndicatorConfig extends SortableEntity implements HasBrand {
  private boolean networkIndicatorEnabled;
  private boolean debugLogEnabled;
  private int pollingInterval;
  private NetworkSpeed networkSpeed;
  private int thresholdTime;
  private int slowTimeout;
  private String imageURL;
  private String brand;
}
