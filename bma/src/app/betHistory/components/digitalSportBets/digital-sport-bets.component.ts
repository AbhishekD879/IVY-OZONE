import { Component, Input, OnDestroy, OnInit, ViewChild } from '@angular/core';
import { DomSanitizer, SafeResourceUrl } from '@angular/platform-browser';

import { PubSubService } from '@core/services/communication/pubsub/pubsub.service';
import { DigitalSportBetsService } from '@core/services/digitalSportBets/digital-sport-bets.service';
import environment from '@environment/oxygenEnvConfig';
import { CoreToolsService } from '@core/services/coreTools/core-tools.service';
import { UserService } from '@core/services/user/user.service';

@Component({
  selector: 'digital-sport-bets',
  templateUrl: 'digital-sport-bets.component.html'
})
export class DigitalSportBetsComponent implements OnInit, OnDestroy {
  @Input() dsTempToken: string;
  @ViewChild('dsIframe', {static: true}) dsIframe: HTMLIFrameElement;

  iframeId: string;
  iframeURL: SafeResourceUrl;

  constructor(
    private userService: UserService,
    private domSanitizer: DomSanitizer,
    private digitalSportSevice: DigitalSportBetsService,
    private pubSubService: PubSubService,
    private coreToolsService: CoreToolsService
  ) {
  }

  ngOnInit(): void {
    const token = this.dsTempToken,
      { username, oddsFormat, currency } = this.userService;
    const iframeUrl = `${environment.DIGITAL_SPORTS_IFRAME_URL}#/mybets/pending/${username}/${token}/${oddsFormat}/${currency}`;
    this.iframeURL = this.domSanitizer.bypassSecurityTrustResourceUrl(iframeUrl);
    this.iframeId = `digitalSportBets${this.coreToolsService.uuid()}`;

    this.pubSubService.subscribe('digitalSportBets', this.pubSubService.API.SET_ODDS_FORMAT, () => {
      this.digitalSportSevice.sendOddsToDS(token, this.dsIframe);
    });
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('digitalSportBets');
  }
}
