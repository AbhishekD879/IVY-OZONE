package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonView;
import com.ladbrokescoral.oxygen.cms.api.entity.projection.view.Views;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "secondarynametoasset")
@NoArgsConstructor
@EqualsAndHashCode(of = {"id"})
public class SecondaryNameToAssetManagement {

  @Id
  @JsonView(Views.GetAll.class)
  private String id;

  @Indexed private String teamName;

  private Integer sportId;

  private String brand;

  private String assetId;

  public SecondaryNameToAssetManagement(
      String teamName, Integer sportId, String brand, String assetId) {
    this.teamName = teamName;
    this.sportId = sportId;
    this.brand = brand;
    this.assetId = assetId;
  }
}
