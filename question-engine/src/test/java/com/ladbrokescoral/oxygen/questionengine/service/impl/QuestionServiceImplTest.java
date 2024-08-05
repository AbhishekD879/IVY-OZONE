package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.configuration.ModelMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;
import com.ladbrokescoral.oxygen.questionengine.exception.NotFoundException;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Question;
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
import static org.mockito.Mockito.when;

@RunWith(MockitoJUnitRunner.class)
public class QuestionServiceImplTest {
  
  @Mock
  private CmsService cmsService;

  private QuestionServiceImpl questionService;
  
  private PodamFactory factory = new PodamFactoryImpl();

  @Before
  public void setUp() {
    this.questionService = new QuestionServiceImpl(cmsService, ModelMapperFactory.getInstance());
  }

  @Test
  public void findQuestionExists() {
    Question question = factory.manufacturePojo(Question.class);
    when(cmsService.findQuestion("1234", "abcd")).thenReturn(Optional.of(question));

    QuestionDto result = questionService.findQuestion("1234", "abcd");
    
    assertNotNull(result);
  }

  @Test(expected = NotFoundException.class)
  public void findQuestionNotExists() {
    when(cmsService.findQuestion("1234", "abcd")).thenReturn(Optional.empty());

    questionService.findQuestion("1234", "abcd");
  }
}
