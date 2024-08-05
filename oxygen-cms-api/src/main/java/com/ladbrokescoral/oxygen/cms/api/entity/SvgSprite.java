package com.ladbrokescoral.oxygen.cms.api.entity;

import lombok.AccessLevel;
import lombok.Getter;
import lombok.RequiredArgsConstructor;

@Getter
@RequiredArgsConstructor(access = AccessLevel.PRIVATE)
/*
!!!IMPORTANT!!! order is critical

UI takes the last one as additional sprite
*/
public enum SvgSprite {
  INITIAL("initial"),
  FEATURED("featured"),
  ADDITIONAL("additional"),
  TIMELINE("timeline"),
  VIRTUAL("virtual");

  private final String spriteName;
}
