package com.ladbrokescoral.oxygen.questionengine.service.impl;

import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;
import com.ladbrokescoral.oxygen.questionengine.exception.NotFoundException;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Question;
import com.ladbrokescoral.oxygen.questionengine.service.QuestionService;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.cms.CmsService;
import lombok.RequiredArgsConstructor;
import org.modelmapper.ModelMapper;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class QuestionServiceImpl implements QuestionService {
  private final CmsService cmsService;
  private final ModelMapper modelMapper;

  @Override
  public QuestionDto findQuestion(String quizId, String questionId) {
    Question question = cmsService.findQuestion(quizId, questionId)
        .orElseThrow(
            () -> new NotFoundException("No Question with id '%s' for quiz with id '%s' found",
                questionId, quizId));

    return modelMapper.map(question, QuestionDto.class);
  }
}
