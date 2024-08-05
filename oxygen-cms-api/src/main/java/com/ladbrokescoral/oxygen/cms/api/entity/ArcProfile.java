package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileData;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import lombok.NonNull;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "arcProfile")
@Data
@EqualsAndHashCode(callSuper = true)
@NoArgsConstructor
public class ArcProfile extends ArcProfileData {

  @NonNull private Integer modelRiskLevel;
  @NonNull private Integer reasonCode;
}
