import {DateAndTimeComponent} from '@app/shared/formElements/dateAndTime/date.time.component';

import {Component, Inject, OnInit, ViewChild} from '@angular/core';
import {BigCompetitionAPIService} from '../../../../../service/big-competition.api.service';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {HttpResponse} from '@angular/common/http';

import {ConfirmDialogComponent} from '@app/shared/dialog/confirm-dialog/confirm-dialog.component';
import {KnockoutsMatch} from '@app/client/private/models/knockoutsmatch.model';
import {RoundNameModel} from '@app/client/private/models/roundName.model';
import {KnockoutEventValid} from '@app/client/private/models/knockouteventvalid.model';
import {CompetitionModule} from '@app/client/private/models/competitionmodule.model';
import {uniqueValidator} from '@app/shared/validators/unique.validator';

@Component({
  selector: 'match-create',
  templateUrl: './match-create.component.html'
})
export class MatchCreateComponent implements OnInit {

  @ViewChild('actionButtons') actionButtons;
  @ViewChild('dateTime') dateTimeComponent: DateAndTimeComponent;

  public form: FormGroup;
  public match: KnockoutsMatch;
  public rounds: Array<RoundNameModel>;
  public roundNames: Array<string>;
  public chosenRound: RoundNameModel;
  public abbreviationOptions: Array<string> = [];
  public initialDate: Date;

  private hasErrors: boolean = false;

  constructor(
    private bigCompetitionApiService: BigCompetitionAPIService,
    @Inject(MAT_DIALOG_DATA) public data: CompetitionModule,
    private dialogRef: MatDialogRef<ConfirmDialogComponent>
  ) {
    this.rounds = this.data.knockoutModuleData.rounds;
    this.roundNames = this.rounds.map(round => round.name);
  }

  ngOnInit() {
    this.initialDate = new Date();
    this.form = new FormGroup({
      eventId: new FormControl(null, []),
      eventName: new FormControl('', []),
      homeTeam: new FormControl('', []),
      homeTeamRemark: new FormControl('', []),
      awayTeam: new FormControl('', []),
      awayTeamRemark: new FormControl('', []),
      venue: new FormControl('', []),
      startTime: new FormControl('', []),
      round: new FormControl('', [Validators.required]),
      abbreviation: new FormControl('', [
        Validators.required,
        uniqueValidator(this.data.knockoutModuleData.events, 'abbreviation', {})
      ]),
    });
    this.getConvertedDate(`${this.initialDate}`);
    this.dateTimeComponent.setDayTime(this.initialDate);
  }

  public closeDialog(): void {
    this.dialogRef.close();
  }

  public getConvertedDate(date: string): void {
    const dateNow = new Date();
    this.form.get('startTime').setValue(`${new Date(new Date(date).getTime() + (dateNow.getTimezoneOffset() * 60000)).toISOString()}`);
  }

  public onChange(): void {
    this.chosenRound = this.rounds[this.rounds.findIndex(round => round.name === this.form.value.round)];
    this.buildAbbreviationSelect(this.chosenRound.abbreviation, Number(this.chosenRound.number));
  }

  public buildAbbreviationSelect(abbreviation: string, count: number): void {
    this.abbreviationOptions = [];
    for (let i: number = 1; i <= count; i++) {
      this.abbreviationOptions.push(abbreviation + i);
    }
  }

  public getSSEvent(event, fromButton: boolean, idFromButton: number): void {
    const eventIdForSS = fromButton ? idFromButton : event.srcElement.value;

    if (eventIdForSS.length || eventIdForSS > 0) {
      this.bigCompetitionApiService.getSiteServeEvent(eventIdForSS)
        .map((response: HttpResponse<KnockoutEventValid>) => {
          return response.body;
        })
        .subscribe((data: KnockoutEventValid) => {
          this.hasErrors = false;
          if (fromButton) {
            this.populateMatch(data);
          }
        }, () => {
          this.form.controls['eventId'].setErrors({'invalid': true});
          this.hasErrors = true;
        });
    }
  }

  public checkForErrors(): void {
    if (this.hasErrors) {
      this.form.controls['eventId'].setErrors({'invalid': true});
      this.hasErrors = false;
    }
  }

  public populateMatch(populateObject): void {
    this.form.get('awayTeam').setValue(populateObject.awayTeam);
    this.form.get('homeTeam').setValue(populateObject.homeTeam);
    this.form.get('eventName').setValue(populateObject.eventName);
    this.form.get('startTime').setValue(populateObject.startTime);
    this.dateTimeComponent.setDayTime(populateObject.startTime);
  }

  public getMatch() {
    return this.form.value;
  }

  public get round(): AbstractControl {
        return this.form.get('round');
  }

  public get abbreviation(): AbstractControl {
       return this.form.get('abbreviation');
  }

  public get eventId(): AbstractControl {
    return this.form.get('eventId');
  }
}
