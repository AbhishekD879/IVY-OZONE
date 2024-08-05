package com.ladbrokescoral.oxygen.notification.services.handler;

import com.ladbrokescoral.oxygen.notification.entities.sportsbook.SportsBookEntity;

public interface AbstractSportsbookUpdateMapper {
  String UPDATE = "update";
  String NON_RUNNER_NAME = " N/R";

  default boolean isUpdate(SportsBookEntity entity) {
    return UPDATE.equals(entity.getMeta().getOperation());
  }
}
