package com.ladbrokescoral.oxygen.questionengine.service.impl;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.questionengine.dto.cms.PrizeDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.exception.QuizRewardNotAssignedException;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.FreebetTriggerResponse;
import com.ladbrokescoral.oxygen.questionengine.service.QuizRewardService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bpp.BppService;
import java.util.Collections;
import java.util.Optional;
import javax.servlet.http.HttpServletRequest;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import uk.co.jemos.podam.api.PodamFactory;
import uk.co.jemos.podam.api.PodamFactoryImpl;

@RunWith(MockitoJUnitRunner.class)
public class QuizRewardServiceImplTest {

  private static final String SOURCE_ID = "/test";
  private static final String HEADER = "token";
  private static final String TOKEN = "11111";
  private static final String PROMOTION_ID = "123456";
  @Mock
  private QuizService quizService;
  @Mock
  private BppService bppService;
  @Mock
  private HttpServletRequest request;

  private PodamFactory factory = new PodamFactoryImpl();
  private QuizRewardService rewardService;
  
  @Before
  public void setUp() {
    rewardService = new QuizRewardServiceImpl(quizService, bppService, request);
    when(quizService.findLiveQuiz(SOURCE_ID)).thenReturn(Optional.of(getQuizDto()));
    when(request.getHeader(HEADER)).thenReturn(TOKEN);
  }

  @Test
  public void assignQuizRewardSuccess() {
    when(bppService.triggerFreebet(TOKEN, PROMOTION_ID)).thenReturn(getFreebetTriggerResponseSuccess());

    rewardService.assignQuizReward(SOURCE_ID);
    
    verify(quizService, times(1)).findLiveQuiz(SOURCE_ID);
    verify(bppService, times(1)).triggerFreebet(TOKEN, PROMOTION_ID);
  }

  @Test(expected = QuizRewardNotAssignedException.class)
  public void assignQuizRewardFailed() {
    when(bppService.triggerFreebet(TOKEN, PROMOTION_ID)).thenReturn(getFreebetTriggerResponseFailed());

    rewardService.assignQuizReward(SOURCE_ID);

  }

  @Test(expected = QuizRewardNotAssignedException.class)
  public void assignQuizRewardNotTriggered() {
    when(bppService.triggerFreebet(TOKEN, PROMOTION_ID)).thenReturn(getFreebetTriggerResponseNotTriggered());

    rewardService.assignQuizReward(SOURCE_ID);

  }
  
  private QuizDto getQuizDto() {
    QuizDto quizDto = factory.manufacturePojo(QuizDto.class);
    quizDto.setCorrectAnswersPrizes(Collections.singletonMap(0, new PrizeDto().setPromotionId(
        PROMOTION_ID)));
    return quizDto;
  }
  
  private FreebetTriggerResponse getFreebetTriggerResponseSuccess() {
    FreebetTriggerResponse response = factory.manufacturePojo(FreebetTriggerResponse.class);
    response.getResponse().getFreebetResponseModel().setFreebetFailure(null);
    response.getResponse().getFreebetResponseModel().getFreebetCalledTrigger().setFreebetTriggerStatus("FIRED");
    return response;
  }

  private FreebetTriggerResponse getFreebetTriggerResponseFailed() {
    FreebetTriggerResponse response = factory.manufacturePojo(FreebetTriggerResponse.class);
    response.getResponse().getFreebetResponseModel().setFreebetCalledTrigger(null);
    return response;
  }

  private FreebetTriggerResponse getFreebetTriggerResponseNotTriggered() {
    FreebetTriggerResponse response = factory.manufacturePojo(FreebetTriggerResponse.class);
    response.getResponse().getFreebetResponseModel().setFreebetFailure(null);
    response.getResponse().getFreebetResponseModel().getFreebetCalledTrigger().setFreebetTriggerStatus("NOT_FIRED");
    return response;
  }
}