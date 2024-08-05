package com.ladbrokescoral.oxygen.cms.api.entity;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.AllSports;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabsTemplate;
import lombok.AllArgsConstructor;
import lombok.Data;

@AllArgsConstructor
@Data
public class SportTabMetaData {

  private MongockTemplate mongockTemplate;
  private String brand;
  private AllSports allSports;
  private SportTabsTemplate sportTabsTemplate;
  private String tabName;
}
