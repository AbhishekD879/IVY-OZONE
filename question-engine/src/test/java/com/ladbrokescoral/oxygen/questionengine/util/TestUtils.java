package com.ladbrokescoral.oxygen.questionengine.util;

import com.ladbrokescoral.oxygen.questionengine.dto.cms.AnswerDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Answer;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Question;

import java.util.Optional;

public class TestUtils {
  public static void buildTree(QuestionDto question) {
    if (!question.getNextQuestions().isEmpty()) {
      String nextQuestionId = question.getNextQuestions()
          .keySet()
          .stream()
          .findAny()
          .orElseThrow(IllegalArgumentException::new);

      question.getAnswers()
          .stream()
          .reduce(Optional.<AnswerDto>empty(), (answer, nextAnswer) -> Optional.of((AnswerDto) nextAnswer.setNextQuestionId(nextQuestionId)), (prev, next) -> next)
          .ifPresent(answer -> buildTree(question.getNextQuestion(answer)));
    }
  }

  public static void buildTree(Question question) {
    if (!question.getNextQuestions().isEmpty()) {
      String nextQuestionId = question.getNextQuestions()
          .keySet()
          .stream()
          .findAny()
          .orElseThrow(IllegalArgumentException::new);

      question.getAnswers()
          .stream()
          .reduce(Optional.<Answer>empty(), (answer, nextAnswer) -> Optional.of(nextAnswer.setNextQuestionId(nextQuestionId)), (prev, next) -> next)
          .ifPresent(answer -> buildTree(question.getNextQuestion(answer)));
    }
  }
}
