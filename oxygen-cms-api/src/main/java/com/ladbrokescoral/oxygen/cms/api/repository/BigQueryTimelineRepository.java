package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.TimelineBigQueryChangelog;

public interface BigQueryTimelineRepository {
  void save(TimelineBigQueryChangelog changelog);
}
