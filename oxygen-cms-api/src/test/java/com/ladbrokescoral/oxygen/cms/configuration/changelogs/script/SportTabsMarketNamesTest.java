package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.exception.MarketNamesMigratorException;
import java.io.IOException;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SportTabsMarketNamesTest {
  @Mock private MongockTemplate mongockTemplate;
  @InjectMocks private SportTabsMarketNamesMigrator sportTabsMarketNamesMigrator;

  @Test(expected = MarketNamesMigratorException.class)
  public void testSaveSportTabsMarketNames() {
    Mockito.when(mongockTemplate.find(Mockito.any(), Mockito.any(), Mockito.any()))
        .thenReturn(null);
    sportTabsMarketNamesMigrator.saveSportsTabMarketNames("ladbrokes");
  }

  @Test(expected = MarketNamesMigratorException.class)
  public void testReadJson() throws IOException {
    sportTabsMarketNamesMigrator.readJson(
        "xyz.json", SportTabsMarketNamesMigrator.SporttabsDto.class);
  }
}
