package com.oxygen.publisher.sportsfeatured.model.module.data;

import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@EqualsAndHashCode(callSuper = true)
public class RpgConfig extends AbstractModuleData {
  private String title;
  private String seeMoreLink;
  private String bundleUrl;
  private String loaderUrl;
  private Integer gamesAmount;
}
