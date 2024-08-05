package com.oxygen.publisher.sportsfeatured.context;

import lombok.Getter;

public enum SportsSocketMessages {

  // TODO:
  GET_FEATURED_STRUCTURE("GET::FEATURED::STRUCTURE"),
  GET_SEGMENTED_FEATURED_STRUCTURE("login"),
  GET_FEATURED_MODULE("GET::FEATURED::MODULE"),
  UPDATE_FEATURED_STRUCTURE("UPDATE::FEATURED::STRUCTURE::%d"),
  UPDATE_FEATURED_MODULE("UPDATE::FEATURED::MODULE::%d"),

  FEATURED_STRUCTURE_CHANGED("FEATURED_STRUCTURE_CHANGED"),
  // This event not following clients update by modular topic in socket room.
  FEATURED_MODULE_CONTENT_CHANGED_MINOR("FEATURED_MODULE_CONTENT_CHANGED_MINOR"),
  ERROR_400("ERROR:400"),
  ERROR_500("FD", "ERROR:500"),
  SUBSCRIBE("subscribe"),
  UNSUBSCRIBE("unsubscribe"),
  APP_VERSION_RESPONSE("version"),
  PAGE_SWITCH("page-switch"),

  PAGE_END("page-end");

  @Getter private final String sportId;

  @Getter private final String code;

  SportsSocketMessages(final String code) {
    this(null, code);
  }

  SportsSocketMessages(final String sportId, final String code) {
    this.sportId = sportId;
    this.code = code;
  }

  public String messageId() {
    if (sportId == null) {
      return code;
    }
    return sportId + ":" + code;
  }
}
