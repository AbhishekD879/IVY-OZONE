import { Injectable } from '@angular/core';
import { VanillaDynamicComponentLoaderService as AppVanillaDynamicComponentLoaderService
} from '@app/vanillaInit/services/vanillaComponentDynamicLoader/vanilla-dynamic-component-loader.service';

@Injectable({
  providedIn: 'root'
})
export class VanillaDynamicComponentLoaderService extends AppVanillaDynamicComponentLoaderService {
  protected VANILLA_HEADER_SLOTS: { [key: string]: string } = {
    betSlip: 'betslip',
    backBtn: 'logo-back'
  };

  protected addComponentsToVanillaHeader(): void {
    // Add betslip icon to Vanilla header dynamically
    this.headerService.whenReady.subscribe(() => {
      //Set header component method is deprecated so registering lazy components like this as per vanilla 16.8.0
      this.headerService['_inner']['dynamicComponentsRegistry'].registerLazyComponent('HEADER','betslip',() => import('@sharedModule/components/betslipHeaderIcon/betslip-header-icon.component').then((x) => x.BetslipHeaderIconComponent));
      this.headerService['_inner']['dynamicComponentsRegistry'].registerLazyComponent('HEADER',this.VANILLA_HEADER_SLOTS.backBtn,() => import('@ladbrokesMobile/shared/components/backButton/back-button.component').then((x) => x.BackButtonComponent));
  });
  }
}
