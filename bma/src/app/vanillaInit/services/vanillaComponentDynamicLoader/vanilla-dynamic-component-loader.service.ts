import { Injectable } from '@angular/core';
import { first } from 'rxjs/operators';
import { UserLoginEvent, UserService } from '@frontend/vanilla/core';
import { HeaderService } from '@frontend/vanilla/core';

@Injectable({
    providedIn: 'root'
})
export class VanillaDynamicComponentLoaderService {

    protected VANILLA_HEADER_SLOTS: { [key: string]: string } = {
        betslip: 'betslip',
        mybets: 'mybets'
    };

    constructor(
      protected user: UserService,
      protected headerService: HeaderService,
    ) {
    }

    init(): void {
        this.user.events.pipe(first(e => e instanceof UserLoginEvent)).subscribe(() => {
            this.addComponentsToVanillaHeader();
        });

        this.addComponentsToVanillaHeader();
    }

    protected addComponentsToVanillaHeader(): void {
        if (this.user.isAuthenticated) {
            // Add betslip icon and my bets button to Vanilla header dynamically
            this.headerService.whenReady.subscribe(() => {
                //Set header component method is deprecated so registering lazy components like this as per vanilla 16.8.0
                this.headerService['_inner']['dynamicComponentsRegistry'].registerLazyComponent('HEADER',this.VANILLA_HEADER_SLOTS.mybets,() => import('@shared/components/myBetsButton/my-bets-button.component').then((x) => x.MyBetsButtonComponent));
                this.headerService['_inner']['dynamicComponentsRegistry'].registerLazyComponent('HEADER','betslip',() => import('@sharedModule/components/betslipHeaderIcon/betslip-header-icon.component').then((x) => x.BetslipHeaderIconComponent));
                return;
            });
        }
        // Add betslip icon to Vanilla header dynamically
        this.headerService.whenReady.subscribe(() => {
            //Set header component method is deprecated so registering lazy components like this as per vanilla 16.8.0
            this.headerService['_inner']['dynamicComponentsRegistry'].registerLazyComponent('HEADER','betslip',() => import('@sharedModule/components/betslipHeaderIcon/betslip-header-icon.component').then((x) => x.BetslipHeaderIconComponent));
        });
    }
}
