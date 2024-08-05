import { BybApiService } from '../services/BYB/byb-api.service';
import { BybHelperService } from '../services/BYB/byb-helper.service';

export interface IYourcallProviders {
  BYB: IBybProvider;
}

export interface IBybProvider {
  api: BybApiService;
  helper: BybHelperService;
}
