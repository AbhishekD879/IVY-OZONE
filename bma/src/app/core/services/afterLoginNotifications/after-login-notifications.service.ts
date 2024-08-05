import { Injectable } from '@angular/core';

import { FreeBetsService } from '@coreModule/services/freeBets/free-bets.service';
import { CommandService } from '@coreModule/services/communication/command/command.service';
import { UserService } from '@core/services/user/user.service';
import { IteratorService } from '@coreModule/services/iterator/iterator.service';
import { Iterator } from '@coreModule/services/iterator/iterator.class';
import { IIteratorItem } from '@coreModule/services/iterator/iterator-item.model';
import { PubSubService } from '@coreModule/services/communication/pubsub/pubsub.service';
import { CmsService } from '@coreModule/services/cms/cms.service';
import { Location } from '@angular/common';
import environment from '@environment/oxygenEnvConfig';
import { IFanzoneComingBack } from '@app/lazy-modules/fanzone/models/fanzone-cb.model';

@Injectable()
export class AfterLoginNotificationsService {
  brand: string = environment.brand;
  notificationDialogs: Array<IIteratorItem> = [{
    priority: 1,
    title: 'fanzoneComingBack',
    description: 'fanzoneComingBack',
    run: (iterator: Iterator) => {
      if (this.brand === 'ladbrokes') {
        this.getFanzoneCbOverlay(iterator);
      } else {
        iterator.next();
      }
    }
  }, 
  
   {
    priority: 2,
    title: 'freeBets',
    description: 'freeBets',
    run: (iterator: Iterator) => {
      this.freeBetInfoShow(iterator);
    }
  }, {
    priority: 3,
    title: 'oddsBoost',
    description: 'Odds boost',
    run: (iterator: Iterator) => {
      this.cmsService.getOddsBoost().subscribe(config => {
        if (config.enabled) {
          this.command.executeAsync(this.command.API.ODDS_BOOST_TOKENS_SHOW_POPUP)
            .finally(() => {
              iterator.next();
            });
        } else {
          iterator.next();
        }
      });
    }
  }, {
    priority: 4,
    title: 'showTimelineSplash',
    description: 'Show timeline splash',
    run: (iterator: Iterator) => {
      this.pubSubService.publish(this.pubSubService.API.SHOW_TIMELINE_TUTORIAL);
      iterator.next();
    }
  }, {
    priority: 5,
    title: 'showExpiryMessage',
    description: 'Show expiry',
    run: () => {
      this.user.set({ quickDepositTriggered: false, loginPending: false });
      this.pubSubService.publish(this.pubSubService.API.LOGIN_POPUPS_END);
    }
  }];

  constructor(
    private freeBetsService: FreeBetsService,
    private command: CommandService,
    private user: UserService,
    private iteratorService: IteratorService,
    private pubSubService: PubSubService,
    private cmsService: CmsService,
    private location: Location
  ) { }

  start(): void {
    // Should run last in the queue - AfterLoginNotificationsService
    setTimeout(() => this.iteratorService.create(this.notificationDialogs).start(), 0);
  }

  /**
   * Show freebet table on successful login
   * @param {Iterator} iterator
   * @returns {void}
   */
  protected freeBetInfoShow(iterator: Iterator): void {
    this.allowedByPath() && this.freeBetsService.showFreeBetsInfo().subscribe(() => {
      iterator.next();
    });
  }

  private allowedByPath(): boolean {
    return !this.location.path().includes('1-2-free');
  }

  /**
   * to display Fanzone Cb overlay for ladbrokes user on login
   * @param iterator - iterator
   */
  private getFanzoneCbOverlay(iterator: Iterator) : void{
    this.cmsService.getFanzoneComingBack().subscribe((comingBackData: IFanzoneComingBack[]) => {
      if (comingBackData[0].fzComingBackPopupDisplay) {
        comingBackData[0]['iterator'] = iterator;
        this.pubSubService.publish(this.pubSubService.API.FANZONE_COMING_BACK, comingBackData);
      } else {
        iterator.next();
      }
    }, (error) => {
      iterator.next();
    });
  }

}
