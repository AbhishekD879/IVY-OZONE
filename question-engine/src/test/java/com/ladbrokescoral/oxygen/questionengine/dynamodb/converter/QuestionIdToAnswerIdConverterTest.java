package com.ladbrokescoral.oxygen.questionengine.dynamodb.converter;

import com.google.common.collect.ImmutableMap;
import org.junit.Test;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;

import static org.assertj.core.api.Assertions.assertThat;

public class QuestionIdToAnswerIdConverterTest {

  private final QuestionIdToAnswerIdConverter questionIdToAnswerIdConverter = new QuestionIdToAnswerIdConverter();

  @Test
  public void convert() {
    String actual = questionIdToAnswerIdConverter.convert(ImmutableMap.of(
        "question-1", Collections.singletonList("answer-1-1"),
        "question-2", Arrays.asList("answer-2-1", "answer-2-2")
    ));

    assertThat(actual).matches(
        "\\{\\s*\"question-1\"\\s*:\\s*"
            + "\\[\\s*\"answer-1-1\"\\s*\\]\\s*,"
            + "\\s*\"question-2\"\\s*:\\s*"
            + "\\[\\s*\"answer-2-1\"\\s*,\\s*\"answer-2-2\"\\s*\\]\\s*\\}"
    );
  }

  @Test
  public void unconvert() {
    Map<String, List<String>> actual = questionIdToAnswerIdConverter.unconvert(
        "{\"question-1\":"
            + "[\"answer-1-1\"],"
            + "\"question-2\":"
            + "[\"answer-2-1\",\"answer-2-2\"]}"
    );

    assertThat(actual).isEqualTo(ImmutableMap.of(
        "question-1", Collections.singletonList("answer-1-1"),
        "question-2", Arrays.asList("answer-2-1", "answer-2-2")
    ));
  }
}
