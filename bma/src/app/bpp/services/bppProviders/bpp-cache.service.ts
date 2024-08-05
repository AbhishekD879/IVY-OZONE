import { Injectable } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import {
  IAccountFreebetsResponse,
  IFreebetToken
} from '@app/bpp/services/bppProviders/bpp-providers.model';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { IFreebestsResponsesCache } from '@app/bpp/services/bpp/bpp.model';

@Injectable()
export class BppCacheService {
  cachedFreebetsResponce: IFreebestsResponsesCache = {};

  constructor(
    private coreToolsService: CoreToolsService,
    private pubSubService: PubSubService
  ) {
  }

  processFreebetsResponce(response: HttpResponse<IAccountFreebetsResponse>): IFreebestsResponsesCache {
    this.cacheAllFreebetsResponses(response.body);
    this.setupCacheRemoveLogic();

    return this.cachedFreebetsResponce;
  }

  setupCacheRemoveLogic(): void {
    this.pubSubService.subscribe('BppCacheService', this.pubSubService.API.SESSION_LOGOUT, () => {
      // cleanup cache on logout
      this.cachedFreebetsResponce = {};
    });

    this.pubSubService.subscribe('BppCacheService', this.pubSubService.API.BET_PLACED, () => {
      // cleanup cache on logout
      this.cachedFreebetsResponce = {};
    });
  }

  private cacheAllFreebetsResponses(allFrebetsResponce: IAccountFreebetsResponse): void  {
    const freeBets = allFrebetsResponce.response.model.freebetToken;
    const freebetsTypes = ['SPORTS', 'ACCESS' , 'BETBOOST'];

    freebetsTypes.forEach((type: string) => {
      this.cachedFreebetsResponce[type] = this.coreToolsService.deepClone(allFrebetsResponce);
      this.cachedFreebetsResponce[type].response.model.freebetToken = [];
    });

    if (freeBets) {
      freeBets.forEach((freebet: IFreebetToken) => {
        const type = freebet.freebetTokenType;

        this.cachedFreebetsResponce[type].response.model.freebetToken.push(freebet);
      });
    }
  }
}
