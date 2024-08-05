package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.configuration.ModelMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.exception.NotFoundException;
import com.ladbrokescoral.oxygen.questionengine.model.cms.QuizHistory;
import com.ladbrokescoral.oxygen.questionengine.configuration.properties.ApplicationProperties;
import com.ladbrokescoral.oxygen.questionengine.service.UpsellService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import uk.co.jemos.podam.api.PodamFactory;
import uk.co.jemos.podam.api.PodamFactoryImpl;

import java.util.Optional;

import static org.junit.Assert.assertNotNull;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@RunWith(MockitoJUnitRunner.class)
public class QuizHistoryServiceImplTest {
  public static final int PREVIOUS_LIMIT = 5;

  @Mock
  private CmsService cmsService;

  @Mock
  private ApplicationProperties properties;

  @Mock
  private UpsellService upsellService;

  private QuizHistoryServiceImpl quizHistoryService;

  private PodamFactory factory = new PodamFactoryImpl();

  @Before
  public void setUp() {
    when(properties.getHistoryPreviousCacheSize()).thenReturn(PREVIOUS_LIMIT);
    when(upsellService.findUpsellFor(any())).thenReturn(Optional.empty());

    quizHistoryService = new QuizHistoryServiceImpl(cmsService, upsellService, ModelMapperFactory.getInstance(), properties);
  }

  @Test
  public void findQuizHistoryExists() {
    QuizHistory quizHistory = factory.manufacturePojo(QuizHistory.class);

    when(cmsService.findHistory("test,quiz", PREVIOUS_LIMIT)).thenReturn(Optional.of(quizHistory));

    AppQuizHistoryDto result = quizHistoryService.findQuizHistory("/test/quiz");

    assertNotNull(result);

  }

  @Test(expected = NotFoundException.class)
  public void findQuizHistoryNotExists() {

    when(cmsService.findHistory("test,quiz", PREVIOUS_LIMIT)).thenReturn(Optional.empty());
    quizHistoryService.findQuizHistory("/test/quiz");
  }
}
