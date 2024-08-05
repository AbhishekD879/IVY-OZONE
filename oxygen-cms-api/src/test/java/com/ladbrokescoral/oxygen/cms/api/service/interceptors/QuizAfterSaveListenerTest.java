package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.QuizDto;
import com.ladbrokescoral.oxygen.cms.api.entity.questionengine.Quiz;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.QuestionEnginePublicService;
import com.ladbrokescoral.oxygen.cms.kafka.LadsCoralKafkaPublisher;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(Parameterized.class)
public class QuizAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Quiz> {
  @Mock private QuestionEnginePublicService service;
  @Getter @InjectMocks private QuizAfterSaveListener listener;
  @Getter @Mock private Quiz entity;
  @Getter @Mock private QuizDto model;

  @Getter private List<QuizDto> collection = Arrays.asList(model);
  @Mock private LadsCoralKafkaPublisher ladsCoralKafkaPublisher;

  @Parameterized.Parameters
  public static List<Object[]> data() throws IOException {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma/question-engine", "quiz"},
          {"connect", "api/connect/question-engine", "quiz"}
        });
  }

  @Before
  public void init() {
    ReflectionTestUtils.setField(listener, "coralQuizTopic", "coral-cms-quiz");
    given(service.getQuizByBrand(anyString())).willReturn(this.getCollection());
  }
}
