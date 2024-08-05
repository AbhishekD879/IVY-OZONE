package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.dto.cms.PrizeDto;
import com.ladbrokescoral.oxygen.questionengine.exception.QuizRewardNotAssignedException;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.BppTokenRequest;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.FreebetTriggerResponse;
import com.ladbrokescoral.oxygen.questionengine.model.bpp.FreebetTriggerResponseModel;
import com.ladbrokescoral.oxygen.questionengine.model.cms.PrizeType;
import com.ladbrokescoral.oxygen.questionengine.service.QuizRewardService;
import com.ladbrokescoral.oxygen.questionengine.service.QuizService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bpp.BppService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Service;

import javax.servlet.http.HttpServletRequest;
import java.util.Objects;
import java.util.Optional;

@RequiredArgsConstructor
@Slf4j
@Service
public class QuizRewardServiceImpl implements QuizRewardService {

  private static final int PROMOTION_REWARD_INDEX = 0;
  private static final String SUCCESS_TRIGGER_MESSAGE = "FIRED";

  private final QuizService quizService;
  private final BppService bppService;
  private final HttpServletRequest request;

  public void assignQuizReward(String quizSourceId) {
    getOnSubmitPrizeConfiguration(quizSourceId)
        .map(PrizeDto::getPromotionId)
        .ifPresent(promotionId -> assignFreebet(quizSourceId, promotionId));
  }

  private void assignFreebet(String quizSourceId, String promotionId) {
    FreebetTriggerResponse response =
        bppService.triggerFreebet(request.getHeader(BppTokenRequest.TOKEN_PROPERTY_NAME), promotionId);

    FreebetTriggerResponseModel responseModel = Optional
        .ofNullable(response.getResponse().getFreebetResponseModel())
        .orElse(new FreebetTriggerResponseModel());

    if (isTriggerNotFired(responseModel)) {
      throw new QuizRewardNotAssignedException(responseModel.getFreebetCalledTrigger().getFreebetTriggerMessage());
    } else if (isTriggerFailed(responseModel)) {
      throw new QuizRewardNotAssignedException(responseModel.getFreebetFailure().getFreebetFailureReason());
    }
    log.info("Free bet assigned for quiz by source id: {}", quizSourceId);
  }

  private boolean isTriggerFailed(FreebetTriggerResponseModel responseModel) {
    return responseModel.getFreebetFailure() != null;
  }

  private boolean isTriggerNotFired(FreebetTriggerResponseModel responseModel) {
    return responseModel.getFreebetCalledTrigger() != null
        && !SUCCESS_TRIGGER_MESSAGE.equalsIgnoreCase(responseModel.getFreebetCalledTrigger().getFreebetTriggerStatus());
  }

  private Optional<PrizeDto> getOnSubmitPrizeConfiguration(String sourceID) {
    return quizService.findLiveQuiz(sourceID)
        .filter(live -> Objects.nonNull(live.getCorrectAnswersPrizes()))
        .filter(live -> live.getCorrectAnswersPrizes().containsKey(PROMOTION_REWARD_INDEX))
        .map(live -> live.getCorrectAnswersPrizes().get(PROMOTION_REWARD_INDEX))
        .filter(prize -> prize.getPrizeType() != PrizeType.NONE)
        .filter(prize -> StringUtils.isNotBlank(prize.getPromotionId()));
  }
}
