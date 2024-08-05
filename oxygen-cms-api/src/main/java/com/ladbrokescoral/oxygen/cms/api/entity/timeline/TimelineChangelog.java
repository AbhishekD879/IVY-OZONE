package com.ladbrokescoral.oxygen.cms.api.entity.timeline;

import com.google.common.base.CaseFormat;
import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.TimelineChangelogOperation;
import java.time.Instant;
import lombok.Data;
import lombok.SneakyThrows;
import lombok.experimental.Accessors;
import org.springframework.data.annotation.Id;

/** A document to record any changes within Timeline feature. */
@Data
@Accessors(chain = true)
public class TimelineChangelog<E extends AbstractEntity> {
  public static final String DOCUMENT_NAME =
      CaseFormat.UPPER_CAMEL.to(CaseFormat.LOWER_CAMEL, TimelineChangelog.class.getSimpleName());

  @Id private String id;
  private TimelineChangelogOperation operation;
  private String type;
  private Instant timestamp;
  private String contentId;
  private E content;

  @SneakyThrows
  public Class<?> getType() {
    return type == null ? null : Class.forName(type);
  }

  public TimelineChangelog<E> setType(Class<?> type) {
    this.type = type.getName();

    return this;
  }
}
