import { Injectable } from '@angular/core';
import { UserService } from '@frontend/vanilla/core';
import { ProductHomepagesConfig } from '@frontend/vanilla/core';
import { UserInterfaceClientConfig } from '@app/client-config/bma-user-interface-config';

@Injectable({
  providedIn: 'root'
})
export class AccountUpgradeLinkService {

  constructor(
    private user: UserService,
    private productHomepagesConfig: ProductHomepagesConfig,
    private userInterfaceConfig: UserInterfaceClientConfig
  ) {}

  get businessPhase(): string {
    return this.user.claims.get('accbusinessphase');
  }
  set businessPhase(value:string){}

  get inShopToMultiChannelLink(): string {
    return this.productHomepagesConfig.portal + this.userInterfaceConfig.accountUpgradeLink.imc;
  }
  set inShopToMultiChannelLink(value:string){}

  get onlineToMultiChannelLink(): string {
    return this.productHomepagesConfig.portal + this.userInterfaceConfig.accountUpgradeLink.omc;
  }
  set onlineToMultiChannelLink(value:string){}
}
