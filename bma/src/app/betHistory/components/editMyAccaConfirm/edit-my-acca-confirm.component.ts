import { Component, Input, OnInit, OnDestroy } from '@angular/core';
import { finalize } from 'rxjs/operators';
import * as _ from 'underscore';

import { EditMyAccaService } from '@app/betHistory/services/editMyAcca/edit-my-acca.service';
import { PubSubService } from '@app/core/services/communication/pubsub/pubsub.service';
import { WindowRefService } from '@app/core/services/windowRef/window-ref.service';

import { IBetHistoryBet, IBetHistoryLeg } from '../../models/bet-history.model';

@Component({
  selector: 'edit-my-acca-confirm',
  templateUrl: './edit-my-acca-confirm.component.html',
  styleUrls: ['./edit-my-acca-confirm.component.scss']
})
export class EditMyAccaConfirmComponent implements OnInit, OnDestroy {
  @Input() bet: { eventSource: IBetHistoryBet, location: string };

  loading: boolean;
  timer: string;

  private timerId: number;

  constructor(
    private editMyAccaService: EditMyAccaService,
    private pubSubService: PubSubService,
    private windowRefService: WindowRefService
  ) {
    this.startTimer = this.startTimer.bind(this);
  }

  get isDisabled(): boolean {
    return this.bet.eventSource.validateBetStatus !== 'ok' ||
      this.hasSuspendedLegs ||
      this.editMyAccaService.hasLegsWithLostStatus(this.bet.eventSource) ||
      !_.some(this.bet.eventSource.leg, (leg: IBetHistoryLeg) => leg.removing);
  }
  set isDisabled(value:boolean) {}

  get hasSuspendedLegs(): boolean {
    return this.editMyAccaService.hasSuspendedLegs(this.bet.eventSource);
  }
  set hasSuspendedLegs(value:boolean) {}
  ngOnInit(): void {
    this.pubSubService.subscribe(
      'EditMyAccaConfirmComponent', this.pubSubService.API.EMA_CONFIRM_NEEDED, this.startTimer
    );
  }

  ngOnDestroy(): void {
    this.pubSubService.unsubscribe('EditMyAccaConfirmComponent');
    this.stopTimer();
  }

  submit(): void {
    if (this.loading) {
      return;
    }

    this.loading = true;
    this.editMyAccaService.editMyAcca(this.bet.eventSource).pipe(
      finalize(() => {
        this.stopTimer();
        this.loading = false;
      })
    ).subscribe();
  }

  // TODO this and related methods could be suppressed by timeService.countDownTimer
  private startTimer(sec: number): void {
    this.timer = this.getTimerValue(sec);
    this.timerId = this.windowRefService.nativeWindow.setInterval(() => {
      sec -= 1;
      this.timer = this.getTimerValue(sec);
    }, 1000);
  }

  private stopTimer(): void {
    this.windowRefService.nativeWindow.clearInterval(this.timerId);
    this.timer = this.timerId = null;
  }

  private getTimerValue(sec: number): string {
    if (sec < 0) {
      return '00:00';
    } else if (sec < 10) {
      return `00:0${sec}`;
    } else {
      return `00:${sec}`;
    }
  }
}
