import { InjectionToken } from '@angular/core';

import { IBrandConfig } from '@core/models/brand-config.model';

export const brandConfigToken = new InjectionToken('brand.config');

export const brandConfig: IBrandConfig = {
    name: 'bma'
};
