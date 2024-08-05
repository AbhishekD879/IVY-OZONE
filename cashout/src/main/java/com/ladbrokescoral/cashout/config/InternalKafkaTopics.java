package com.ladbrokescoral.cashout.config;

public enum InternalKafkaTopics {
  BET_UDPATES("bet-updates"),
  BET_DETAIL_REQUESTS("bet-detail-requests"),
  BET_UPDATES_ERRORS("bet-updates-errors"),
  CASHOUT_OFFER_REQUESTS("cashout-offer-requests"),
  PAYOUT_UDPATES("payout-updates"),
  EVENT_UPDATES("event-updates"),
  TWOUP_UPDATES("twoup_updates");

  private final String topicName;

  InternalKafkaTopics(String topicName) {
    this.topicName = topicName;
  }

  public String getTopicName() {
    return topicName;
  }
}
