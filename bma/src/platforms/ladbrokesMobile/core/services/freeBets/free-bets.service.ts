import { Injectable } from '@angular/core';
import { FreeBetsService as AppFreeBetsService } from '@core/services/freeBets/free-bets.service';
import { SiteServerService } from '@core/services/siteServer/site-server.service';
import { ModuleExtensionsStorageService } from '@core/services/moduleExtensionsStorage/module-extensions-storage.service';
import { UserService } from '@core/services/user/user.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { StorageService } from '@core/services/storage/storage.service';
import { SessionService } from '@authModule/services/session/session.service';
import { TimeService } from '@core/services/time/time.service';
import { BppService } from '@app/bpp/services/bpp/bpp.service';
import { NativeBridgeService } from '@core/services/nativeBridge/native-bridge.service';
import { DialogService } from '@core/services/dialogService/dialog.service';
import { RoutingHelperService } from '@core/services/routingHelper/routing-helper.service';
import { FiltersService } from '@core/services/filters/filters.service';
import { IFreebetToken } from '@app/bpp/services/bppProviders/bpp-providers.model';
import { LocaleService } from '@core/services/locale/locale.service';
import { DeviceService } from '@core/services/device/device.service';
import { SportsConfigHelperService } from '@sb/services/sportsConfig/sport-config-helper.service';

@Injectable()
export class FreeBetsService extends AppFreeBetsService {
  constructor(
    protected siteServerService: SiteServerService,
    protected modulesExtensionsStorage: ModuleExtensionsStorageService,
    protected user: UserService,
    protected pubsubService: PubSubService,
    protected storage: StorageService,
    protected sessionService: SessionService,
    protected timeService: TimeService,
    protected bppService: BppService,
    protected nativeBridge: NativeBridgeService,
    protected dialogService: DialogService,
    protected routingHelperService: RoutingHelperService,
    protected filtersService: FiltersService,
    protected locale: LocaleService,
    protected deviceService: DeviceService,
    protected sportsConfigHelperService: SportsConfigHelperService
  ) {
    super(
      siteServerService,
      modulesExtensionsStorage,
      user,
      pubsubService,
      storage,
      sessionService,
      timeService,
      bppService,
      nativeBridge,
      dialogService,
      routingHelperService,
      filtersService,
      locale,
      deviceService,
      sportsConfigHelperService
    );
  }

  protected enhanceFreeBetItem(item: IFreebetToken): IFreebetToken {
    if (item.freebetTokenExpiryDate) {
      const tempDate = new Date(item.freebetTokenExpiryDate.replace(/-/g, '/'));
      const timeDifferent = this.timeService.compareDate(item.freebetTokenExpiryDate);
      if (timeDifferent > 7) {
        item.usedBy = this.timeService.formatByPattern(tempDate, 'dd/MM/yyyy');
      } else {
        item.freebetTokenExpiryDate = this.timeService.formatByPattern(tempDate, 'yyyy-MM-dd HH:mm:ss');
        item.expires = `${timeDifferent} day${timeDifferent > 1 ? 's' : ''}`;
      }
    }
    item.freeBetType = this.getFreeBetType(item);
    return item;
  }
}
