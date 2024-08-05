package com.coral.oxygen.middleware.ms.quickbet.impl;

import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.coral.oxygen.middleware.ms.liveserv.utils.StringUtils;
import java.util.ArrayList;
import java.util.List;

public class LiveServChannelUtils {

  private LiveServChannelUtils() {}

  public static List<String> calculateLiveServChannels(
      String outcomeId, String marketId, String eventId) {
    List<String> result = new ArrayList<>();
    result.add(ChannelType.sEVENT.getName() + StringUtils.addLeadingZeros(eventId, 10));
    result.add(ChannelType.sSCBRD.getName() + StringUtils.addLeadingZeros(eventId, 10));
    result.add(ChannelType.sCLOCK.getName() + StringUtils.addLeadingZeros(eventId, 10));
    result.add(ChannelType.sEVMKT.getName() + StringUtils.addLeadingZeros(marketId, 10));
    result.add(ChannelType.sSELCN.getName() + StringUtils.addLeadingZeros(outcomeId, 10));
    return result;
  }
}
