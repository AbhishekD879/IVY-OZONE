import { ClientConfig, ClientConfigProductName } from '@frontend/vanilla/core';

@ClientConfig({
  key: 'bmaUserInterfaceConfig',
  product: ClientConfigProductName.SPORTS,
  reload: false
} as any)
export class UserInterfaceClientConfig {
  rtsLink: string;
  accountUpgradeLink: {
    imc: string;
    omc: string;
  };
  cspSegmentExpiry: number;
  homeBiometric: {
    android: boolean,
    ios: boolean 
  }
}
