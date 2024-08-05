
import { IRetailConfig, ISystemConfig } from '@core/services/cms/models/system-config';

export interface ILadbrokesSystemConfig extends ISystemConfig {
  Connect: ILadbrokesRetailConfig;
}


export interface ILadbrokesRetailConfig extends IRetailConfig {
  raceBetFinder: boolean;
  digitalCoupons: boolean;
  savedBetCodes: boolean;
  betCalculator: boolean;
}
