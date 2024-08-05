package com.ladbrokescoral.oxygen.cms.api.entity.timeline;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import java.time.Instant;

public interface Auditable<E extends AbstractEntity & Auditable<E>> {
  String getId();

  String getUpdatedByUserName();

  Instant getUpdatedAt();

  E content();
}
