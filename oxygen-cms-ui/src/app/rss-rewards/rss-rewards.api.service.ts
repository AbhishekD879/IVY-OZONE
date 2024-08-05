import {Injectable} from '@angular/core';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';
import { ApiClientService } from '../client/private/services/http';
import { RssRewards } from '@app/client/private/models/coins-rewards.model';

@Injectable()
export class RssRewardsApiService {
  constructor(
    private apiClientService: ApiClientService
  ) {
  }
  get() {
    return this.apiClientService.rssRewards().get();
  }
  create(rssRewards: RssRewards) {
    return this.apiClientService.rssRewards().create(rssRewards);
  }

  update(rssRewards: RssRewards) {
    return this.apiClientService.rssRewards().update(rssRewards);
  }
}
