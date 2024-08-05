package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.timeline.TimelineChangelog;
import java.util.Objects;

public interface TimelineChangelogSubscription<E extends AbstractEntity> {
  void subscribe(TimelineChangelog<E> changelog);

  Class<E> type();

  default boolean isSupportedChange(TimelineChangelog<E> changelog) {
    return Objects.nonNull(changelog)
        && Objects.nonNull(changelog.getType())
        && changelog.getType().isAssignableFrom(type());
  }
}
