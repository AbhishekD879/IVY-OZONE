package com.coral.oxygen.middleware.common.service.notification.topic;

import lombok.AccessLevel;
import lombok.RequiredArgsConstructor;

@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
public enum TopicType {
  FEATURED_STRUCTURE_CHANGED,
  FEATURED_MODULE_CONTENT_CHANGED,
  FEATURED_MODULE_CONTENT_CHANGED_MINOR,
  SPORTS_FEATURED_PAGE_DELETED,
  SPORTS_FEATURED_PAGE_ADDED,
  FEATURED_LIVE_SERVER_MODULES("live_server_featured_modules"),

  IN_PLAY_STRUCTURE_CHANGED,
  IN_PLAY_SPORT_SEGMENT_CHANGED,
  IN_PLAY_SPORTS_RIBBON_CHANGED,
  IN_PLAY_SPORT_COMPETITION_CHANGED,
  INPLAY_LIVE_SERVER_MODULES("live_server_inplay_modules"),

  VIRTUAL_SPORTS_RIBBON_CHANGED;

  private final String name;

  TopicType() {
    this.name = name();
  }

  public String getTopicName() {
    return name;
  }
}
