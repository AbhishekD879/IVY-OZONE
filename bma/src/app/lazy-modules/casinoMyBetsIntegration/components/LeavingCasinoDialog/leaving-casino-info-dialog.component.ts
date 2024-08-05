import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { LocaleService } from '@core/services/locale/locale.service';
import environment from '@environment/oxygenEnvConfig';
import { bma } from '@app/lazy-modules/locale/translations/en-US/bma.lang';
import { ConfirmationDialogEmit } from '@app/betHistory/services/CasinoMyBetsIntegratedService/casino-mybets-integrated.service';
@Component({
  selector: 'leaving-casino-info-dialog',
  templateUrl: './leaving-casino-info-dialog.component.html',
  styleUrls: ['./leaving-casino-info-dialog.component.scss']
})
export class LeavingCasinoDialogComponent implements OnInit {
  @Input() showLeavingCasinoDialog: boolean;
  @Output() readonly userAction: EventEmitter<{btnClicked: string, checkboxValue: boolean}>
   = new EventEmitter<{btnClicked: string, checkboxValue: boolean}>();
  isBrandLadbrokes: boolean;
  dontShowPopupAgain: boolean = false;
  emitObj: ConfirmationDialogEmit;

  constructor(private locale: LocaleService) { }

  ngOnInit(): void {
    this.isBrandLadbrokes = environment.brand === this.locale.getString(bma.brands.ladbrokes).toLowerCase();
  }

  /**
   * click handler for NoThanks/ yesyletsgo button
  */
  popupClickHandler(event: MouseEvent, btnclickText: string): void {
    event.stopPropagation();
    this.emitObj = {
      btnClicked: btnclickText,
      checkboxValue: this.dontShowPopupAgain
    };

    this.userAction.emit(this.emitObj);
  }
}
