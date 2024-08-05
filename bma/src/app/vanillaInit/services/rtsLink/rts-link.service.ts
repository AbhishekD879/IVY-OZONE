import { Injectable } from '@angular/core';

import { ProductHomepagesConfig } from '@frontend/vanilla/core';
import { UserInterfaceClientConfig } from '@app/client-config/bma-user-interface-config';

@Injectable({
  providedIn: 'root'
})
export class RtsLinkService {

  constructor(
    private productHomepagesConfig: ProductHomepagesConfig,
    private userInterfaceConfig: UserInterfaceClientConfig
  ) {}

  getRtsLink(): string {
    return this.productHomepagesConfig.portal + this.userInterfaceConfig.rtsLink;
  }
}
