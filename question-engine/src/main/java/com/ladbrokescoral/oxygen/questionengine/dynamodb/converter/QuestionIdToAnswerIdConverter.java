package com.ladbrokescoral.oxygen.questionengine.dynamodb.converter;

import com.amazonaws.services.dynamodbv2.datamodeling.DynamoDBTypeConverter;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.questionengine.configuration.ObjectMapperFactory;
import lombok.SneakyThrows;

import java.util.List;
import java.util.Map;

public class QuestionIdToAnswerIdConverter implements DynamoDBTypeConverter<String, Map<String, List<String>>> {
  private static final ObjectMapper OBJECT_MAPPER = ObjectMapperFactory.getInstance();

  @Override
  @SneakyThrows
  public String convert(Map<String, List<String>> object) {
    return OBJECT_MAPPER.writeValueAsString(object);
  }

  @Override
  @SneakyThrows
  public Map<String, List<String>> unconvert(String object) {
    return OBJECT_MAPPER.readValue(object, new TypeReference<Map<String, List<String>>>() {
    });
  }
}
