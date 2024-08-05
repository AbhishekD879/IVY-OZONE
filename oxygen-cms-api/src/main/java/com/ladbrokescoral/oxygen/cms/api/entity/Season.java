package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "season")
@Data
@EqualsAndHashCode(callSuper = true)
public class Season extends AbstractEntity implements HasBrand {

  @Brand private String brand;

  @NotBlank private String seasonName;

  @NotBlank private String seasonInfo;

  @NotNull private Instant displayFrom;

  @NotNull private Instant displayTo;
}
