package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "teamKits")
@AllArgsConstructor
@NoArgsConstructor
public class TeamKit extends AbstractEntity {

  @NotBlank @Brand private String brand;
  @NotBlank private String teamName;
  private String path;
  private String svg;
  private String svgId;
}
