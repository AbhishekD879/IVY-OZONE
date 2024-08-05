import { Component, OnInit, ComponentFactoryResolver } from '@angular/core';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { FanzoneSharedService } from '@lazy-modules/fanzone/services/fanzone-shared.service';
import { IFanzoneSyc } from '@lazy-modules/fanzone/models/fanzone-syc.model';
import { FanzoneSycDialogComponent } from './fanzoneSycDialog/fanzone-syc-dialog.component';
import { DialogService } from '@app/core/services/dialogService/dialog.service';
import { UserService } from '@core/services/user/user.service';
import { WindowRefService } from '@core/services/windowRef/window-ref.service';
import { FanzoneHelperService } from '@app/core/services/fanzone/fanzone-helper.service';

@Component({
  selector: 'fanzone-shared',
  template: ``
})
export class FanzoneSharedComponent implements OnInit {
  sycData: IFanzoneSyc[];
  channelName = 'fanzoneSharedHome';

  constructor(private fanzoneSharedService: FanzoneSharedService,
    private pubsub: PubSubService,
    private dialogService: DialogService,
    private User: UserService,
    private windowRefService: WindowRefService,
    private componentFactoryResolver: ComponentFactoryResolver,
    private fanzoneHelperService: FanzoneHelperService
  ) { }

  /**
   * to initiate the logic on component initialisation
   * @returns {void}
   */
  ngOnInit(): void {
    this.getSycData();
    this.pubsub.subscribe(this.channelName, [this.pubsub.API.SESSION_LOGIN, this.pubsub.API.SUCCESSFUL_LOGIN], () => {
      this.fanzoneHelperService.fanzoneTeamUpdate.subscribe(() => {
        this.getSycData();
      });
      this.fanzoneHelperService.checkIfTeamIsRelegated().subscribe((isTeamRelegated) => {
        isTeamRelegated && this.getSycData();
      });
    });
  }

  /**
   * get syc data and publish it
   * @returns {void}
   */
  getSycData(): void {
    this.fanzoneSharedService.getSpecialPagesDataCollection().subscribe((fzData: IFanzoneSyc[]) => {
      this.sycData = fzData;

      this.showFanzoneSyc(this.sycData);
    });
  }

  /**
    * This method is used to get fanzone syc
    * @returns {void}
    */
  private showFanzoneSyc(sycData): void {
    const componentFactory = this.componentFactoryResolver.resolveComponentFactory(FanzoneSycDialogComponent);
    const isFootballPage = this.windowRefService.nativeWindow.location.pathname === '/sport/football' || this.windowRefService.nativeWindow.location.href.includes('/sport/football/matches');
    this.fanzoneSharedService.isFanzoneConfigDisabled().subscribe((isDisabled) => {
      if (isFootballPage && !!this.User.username && !!this.sycData && !isDisabled) {
        this.dialogService.openDialog('SYT', componentFactory, true, sycData[0]);
      }
    })

  }

  ngOnDestroy() {
    this.pubsub.unsubscribe(this.channelName);
  }
}
