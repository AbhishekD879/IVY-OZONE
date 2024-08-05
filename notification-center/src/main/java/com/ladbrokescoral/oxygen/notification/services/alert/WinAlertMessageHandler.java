package com.ladbrokescoral.oxygen.notification.services.alert;

import com.ladbrokescoral.oxygen.notification.entities.bet.Betslip;

/**
 * Handles messages from DF kafka (betslip topic). Checks if the message is telling that the bet has
 * some winning amount, and if yes, checks if that bet is among subscribers, in that case, this
 * handler will try to send push notification via {@see NotificationsFactory.class}
 */
public interface WinAlertMessageHandler {
  void handleBetslip(Betslip betslip);
}
