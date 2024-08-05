import { ClientConfig, ClientConfigProductName } from '@frontend/vanilla/core';

@ClientConfig({
  key: 'bmaHtmlInjectionConfig',
  product: ClientConfigProductName.SPORTS,
  reload: false
} as any)
export class HtmlInjectionConfig {
  headTags: any;
}
