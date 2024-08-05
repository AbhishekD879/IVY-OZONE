package com.ladbrokescoral.oxygen.cms.api.entity;

import static org.junit.Assert.assertEquals;

import org.junit.Test;

public class CompetitionSubTabTest {

  @Test
  public void populatePathFromExistingEntity() {
    CompetitionSubTab existingEntity = new CompetitionSubTab();
    existingEntity.setPath("/competitionUri/tabUri/subTabUri");
    existingEntity.setUri("/subTabUri");

    CompetitionSubTab updateEntity = new CompetitionSubTab();
    updateEntity.setUri("/newSubTabUri");

    CompetitionSubTab updateEntityWithPath = updateEntity.setPathFromExistingEntity(existingEntity);
    assertEquals("/competitionUri/tabUri/newSubTabUri", updateEntityWithPath.getPath());
  }
}
