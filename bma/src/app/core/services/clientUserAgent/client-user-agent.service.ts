import { Injectable } from '@angular/core';
import { DeviceService } from '@core/services/device/device.service';

import { CLIEN_USER_AGENT_IDS } from '@core/constants/client-user-agent-ids.constant';

@Injectable()
export class ClientUserAgentService {

  constructor(private device: DeviceService) {}

  /**
   * Get client user agent id
   * @param isVirtual: boolean
   * @param isLotto: boolean
   */
  getId(isVirtual: boolean = false, isLotto: boolean = false): string {
    let clientUserAgent: string = '';
    if (this.device.isDesktop) {
      clientUserAgent = this.getDesktopId(isVirtual, isLotto);
    } else if (this.device.isWrapper) {
      clientUserAgent = this.getWrapperId;
    } else if (this.device.isMobile || this.device.isTablet) {
      clientUserAgent = this.getMobileId;
    }

    return clientUserAgent;
  }

  /**
   * Get mobile client user agent id
   */
  private get getMobileId(): string {
    if (this.device.isIos) {
      return CLIEN_USER_AGENT_IDS.mobile.ios;
    }

    return CLIEN_USER_AGENT_IDS.mobile.android;
  }
private set getMobileId(value:string){}
  /**
   * Get wrapper client user agent id
   */
  private get getWrapperId(): string {
    if (this.device.isIos) {
      return CLIEN_USER_AGENT_IDS.wrapper.ios;
    }

    return CLIEN_USER_AGENT_IDS.wrapper.android;
  }
private set getWrapperId(value:string){}
  /**
   * Get desktop client user agent id, detect if bet was placed from lotto/virtuals/regular
   */
  private getDesktopId(isVirtual: boolean, isLotto: boolean): string {
    let desktopClientUserAgentId = '';

    if (isVirtual) {
      desktopClientUserAgentId = this.device.isDesktopWindows
        ? CLIEN_USER_AGENT_IDS.desktop.virtualsWindows
        : CLIEN_USER_AGENT_IDS.desktop.virtualsOSX;
    } else if (isLotto) {
      desktopClientUserAgentId = this.device.isDesktopWindows
        ? CLIEN_USER_AGENT_IDS.desktop.lottoWindows
        : CLIEN_USER_AGENT_IDS.desktop.lottoOSX;
    } else {
      desktopClientUserAgentId = this.device.isDesktopWindows
        ? CLIEN_USER_AGENT_IDS.desktop.windows
        : CLIEN_USER_AGENT_IDS.desktop.osX;
    }

    return desktopClientUserAgentId;
  }
}
