package com.coral.oxygen.middleware.ms.liveserv.impl;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.model.ChannelType;
import com.coral.siteserver.api.SiteServerService;
import com.coral.siteserver.model.SSResponse;
import org.springframework.beans.factory.annotation.Autowired;
import retrofit2.Call;

/** Created by azayats on 08.05.17. */
public class SiteServEventIdResolver extends BaseEventIdResolver implements OldEventIdResolver {
  @Autowired SiteServerService service;

  @Override
  public long resolve(ChannelType type, long id) throws ServiceException {
    Call<SSResponse> call;
    switch (type) {
      case sEVMKT:
      case SEVMKT:
        call = service.getMarketCall(id);
        break;
      case sSELCN:
      case SSELCN:
      case sPRICE:
        call = service.getSelectionCall(id);
        break;
      default:
        return super.resolve(type, id);
    }
    return service.getEventId(call);
  }
}
