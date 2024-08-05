package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "maintenancepagenotifications")
@Data
@EqualsAndHashCode(callSuper = true)
public class MaintenancePageNotification extends AbstractEntity implements HasBrand {

  @NotBlank private String brand;
  @NotNull private Instant triggeredDate;
  private boolean activateMaintenance;
  private long ttlSeconds;
  private String url;
  private String status;
}
