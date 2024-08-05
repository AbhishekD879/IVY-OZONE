package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.experimental.SuperBuilder;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "dashboards")
@Data
@NoArgsConstructor
@SuperBuilder
@EqualsAndHashCode(callSuper = true)
public class Dashboard extends AbstractEntity {
  private Integer estimatedTime;
  @NotBlank private Integer status;
  private String message;
  private String purgeID;
  private String progressURI;
  private String supportID;
  @NotBlank private String type;
  @NotBlank private String domains;
  private Instant currentTime;
  private String brand;
}
