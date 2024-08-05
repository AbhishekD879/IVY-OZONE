package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import java.util.Collections;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SegmentedModuleCreateTest {

  @Mock private MongockTemplate mongockTemplate;

  @InjectMocks private SegmentedModuleCreate segmentedModuleCreate;

  @Before
  public void init() {
    Mockito.when(mongockTemplate.insert(Mockito.any(), Mockito.anyString()))
        .thenReturn(Collections.emptyList());
  }

  @Test
  public void testAddSegmentedModule() {
    segmentedModuleCreate.addSegmentedModule(mongockTemplate, "bma");
    Mockito.verify(mongockTemplate, Mockito.times(1)).insert(Mockito.any(), Mockito.anyString());
  }
}
