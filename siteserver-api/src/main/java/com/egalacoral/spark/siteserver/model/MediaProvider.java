package com.egalacoral.spark.siteserver.model;

import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = true)
public class MediaProvider extends IdentityWithChildren {

  private String id;
  private String name;
  private String mediaTypeCode;
  private String listingUrl;

  public List<Media> getMedia() {
    return getConcreteChildren(Children::getMedia);
  }
}
