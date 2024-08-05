import { Injectable } from '@angular/core';

import { SeoDataService as AppSeoDataService } from '@core/services/seoData/seo-data.service';
import { ISeoPage } from '@core/services/cms/models';

@Injectable({
  providedIn: 'root'
})
export class SeoDataService extends AppSeoDataService {
  defaultPage: Partial<ISeoPage> = {
    title: 'Ladbrokes Sports Betting - Football, Horse Racing and more!',
    description: 'Sports betting odds at Ladbrokes Sports. View for tips, available match odds, ' +
      'live-results and more. Football, Horse Racing and more! Bet now with Ladbrokes!'
  };
}

