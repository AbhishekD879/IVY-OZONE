package com.ladbrokescoral.oxygen.questionengine.configuration;

import com.ladbrokescoral.oxygen.questionengine.dto.cms.AnswerDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.AppQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.cms.QuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.AnsweredQuestionDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.SubmittedAnswerDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizDto;
import com.ladbrokescoral.oxygen.questionengine.dto.userquiz.UserQuizHistoryDto;
import com.ladbrokescoral.oxygen.questionengine.model.cms.Question;
import lombok.RequiredArgsConstructor;
import lombok.experimental.UtilityClass;
import org.modelmapper.AbstractConverter;
import org.modelmapper.ModelMapper;
import org.modelmapper.PropertyMap;
import org.modelmapper.convention.MatchingStrategies;

import java.util.AbstractMap;
import java.util.Map;
import java.util.stream.Collectors;

@UtilityClass
public class ModelMapperFactory {

  public static ModelMapper getInstance() {
    ModelMapper modelMapper = new ModelMapper();

    modelMapper.getConfiguration()
        .setMatchingStrategy(MatchingStrategies.STRICT);

    modelMapper
        .createTypeMap(AppQuizHistoryDto.class, UserQuizHistoryDto.class)
        .addMappings(mapper -> {
          mapper.skip(UserQuizHistoryDto::setLive);
          mapper.skip(UserQuizHistoryDto::setPrevious);
          mapper.skip(UserQuizHistoryDto::setPreviousCount);
        });
    modelMapper.createTypeMap(QuizDto.class, UserQuizDto.class)
        .addMappings(mapper -> mapper.skip(UserQuizDto::setFirstAnsweredQuestion));
    modelMapper.createTypeMap(AnswerDto.class, SubmittedAnswerDto.class)
        .addMappings(mapper -> mapper.skip(SubmittedAnswerDto::setUserChoice));

     /*
      For some reason Model Mapper is unable to map Map<String, Question[Dto]> correctly, duh...
     */
    modelMapper.createTypeMap(Question.class, QuestionDto.class)
        .addMappings(new PropertyMap<Question, QuestionDto>() {
          @Override
          protected void configure() {
            using(new StringKeyedMapConverter<>(modelMapper, QuestionDto.class)).map(source.getNextQuestions(), destination.getNextQuestions());
          }
        });
    modelMapper.createTypeMap(QuestionDto.class, AnsweredQuestionDto.class)
        .addMappings(new PropertyMap<QuestionDto, AnsweredQuestionDto>() {
          @Override
          protected void configure() {
            using(new StringKeyedMapConverter<>(modelMapper, AnsweredQuestionDto.class)).map(source.getNextQuestions(), destination.getNextQuestions());
        }
        });

    return modelMapper;
  }


  @RequiredArgsConstructor
  private static class StringKeyedMapConverter<D> extends AbstractConverter<Map<String, ?>, Map<String, D>> {
    private final ModelMapper modelMapper;
    private final Class<? extends D> destinationType;

    @Override
    protected Map<String, D> convert(Map<String, ?> source) {
      return source.entrySet()
          .stream()
          .map(idToQuestion -> new AbstractMap.SimpleImmutableEntry<>(
              idToQuestion.getKey(),
              modelMapper.map(idToQuestion.getValue(), destinationType))
          )
          .collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
    }
  }
}
