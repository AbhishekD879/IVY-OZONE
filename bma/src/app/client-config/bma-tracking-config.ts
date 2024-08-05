import { ClientConfig, ClientConfigProductName } from '@frontend/vanilla/core';

@ClientConfig({
  key: 'bmaTrackingConfig',
  product: ClientConfigProductName.SPORTS,
  reload: false
} as any)
export class TrackingConfig {
  gtmConfigs: any;
  awsConfigs: any;
}
