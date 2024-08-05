package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.time.Instant;
import java.util.HashMap;
import java.util.Map;
import lombok.Data;
import lombok.RequiredArgsConstructor;
import lombok.experimental.Accessors;

@Data
@Accessors(chain = true)
public class TimelineBigQueryChangelog {
  private static final ObjectMapper CONTENT_CONVERTER =
      new ObjectMapper()
          .findAndRegisterModules()
          .setDefaultPropertyInclusion(JsonInclude.Include.NON_NULL);

  private String id;
  private String username;
  private Instant createdDate;
  private TimelineChangelogOperation operation;
  private Class<?> type;
  private AbstractEntity entity;

  public Map<String, Object> asJson() throws JsonProcessingException {
    Map<String, Object> json = new HashMap<>();

    json.put(Column.ID.columnName, id);
    json.put(Column.USERNAME.columnName, username);
    json.put(Column.CREATED_DATE.columnName, createdDate.toString());
    json.put(Column.OPERATION.columnName, operation.name());
    json.put(Column.TYPE.columnName, type.getSimpleName());

    if (operation != TimelineChangelogOperation.DELETE) {
      json.put(Column.CONTENT.columnName, CONTENT_CONVERTER.writeValueAsString(entity));
    }
    return json;
  }

  @RequiredArgsConstructor
  private enum Column {
    ID("ID", 0),
    USERNAME("Username", 1),
    CREATED_DATE("CreatedDate", 2),
    OPERATION("Operation", 3),
    TYPE("Type", 4),
    CONTENT("Content", 5);

    final String columnName;
    final int columnPosition;
  }
}
