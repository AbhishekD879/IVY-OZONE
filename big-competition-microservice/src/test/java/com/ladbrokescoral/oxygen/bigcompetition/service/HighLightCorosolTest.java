package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.HighlightCarouselModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.HighlightCarouselServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class HighLightCorosolTest {

  private HighlightCarouselServiceImpl highlightCarouselService;

  @Before
  public void init() {
    highlightCarouselService = new HighlightCarouselServiceImpl();
  }

  @Test
  public void testHightlightCorosolFromCms() {

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionPromotionsService/highlighCorosolInput.json", CompetitionModule.class);
    HighlightCarouselModuleDto moduleDto = this.highlightCarouselService.process(competitionModule);
    Assert.assertNotNull(moduleDto);
  }
}
