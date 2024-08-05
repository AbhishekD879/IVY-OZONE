package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "svgimages")
@Data
@EqualsAndHashCode(callSuper = true)
@CompoundIndex(name = "brand_svgId", def = "{'brand' : 1, 'svgId': 1}", unique = true)
public class SvgImage extends AbstractEntity implements SvgAbstractMenu {

  private String brand;
  private boolean active = true;
  private String svgId;
  private String sprite;
  private String description;
  private SvgFilename svgFilename;
  private String svg;
}
