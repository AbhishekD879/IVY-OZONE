package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import static org.mockito.Mockito.when;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.configuration.changelogs.DatabaseChangeLog;
import java.util.ArrayList;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SportCategoriesArchivalCreateTest {

  @Mock private MongockTemplate mongockTemplate;

  // @InjectMocks private UpdateHomeModuleSortOrder segmentedModuleCreate;

  @InjectMocks private DatabaseChangeLog databaseChangeLog;

  @Before
  public void init() {}

  @Test
  public void testUpdateHomeModule() {

    when(mongockTemplate.findAll(HomeModule.class, "homemodules")).thenReturn(getHomeModules(10.0));
    databaseChangeLog.updateSortOrderForHomeModules(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(0)).save(Mockito.any());
  }

  @Test
  public void testUpdateHomeModuleWithSortNull() {

    when(mongockTemplate.findAll(HomeModule.class, "homemodules")).thenReturn(getHomeModules(null));
    databaseChangeLog.updateSortOrderForHomeModules(mongockTemplate);
    Mockito.verify(mongockTemplate, Mockito.times(1)).save(Mockito.any());
  }

  public List<HomeModule> getHomeModules(Double Doublr) {

    HomeModule module = new HomeModule();
    module.setSortOrder(Doublr);
    module.setDisplayOrder(10.0);
    List<HomeModule> modules = new ArrayList<>();
    modules.add(module);
    return modules;
  }
}
