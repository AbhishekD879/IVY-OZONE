import { Component, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Inject } from '@angular/core';
import { ISportAction } from '@root/app/client/private/models/arcConfig.model';
@Component({
  selector: 'app-arc-sport-actions-pop-up',
  templateUrl: './arc-sport-actions-pop-up.component.html',
  styleUrls: ['./arc-sport-actions-pop-up.component.scss']
})
export class ArcSportActionsPopUpComponent implements OnInit {
  public addData: ISportAction[];
  linkEX: string = 'eg: Lorem ipsum dolor sit amet $LINK Gambling Controls. $LINK'
  constructor(@Inject(MAT_DIALOG_DATA) public data: { sports: ISportAction[], sportsArray: ISportAction[] }) { }

  ngOnInit(): void {
    this.data.sportsArray.map((sportValues: ISportAction) => {
      this.data.sports.forEach((data: ISportAction) => {
        if (data.action === sportValues.action) {
          sportValues.enabled = data.enabled;
          sportValues.messagingContent = data.messagingContent;
          sportValues.gcLink = data.gcLink;
        }
      });
    });
    this.addData = this.data.sports;
  }
  addSport(sportAction: ISportAction): void {
    this.addData.map((item, index) => {
      if (item.action === sportAction.action) {
        this.addData.splice(index);
      }
    });
    if (sportAction.enabled) {
      this.addData.push(sportAction);
    }
  }
  isValid(item: ISportAction): boolean {
    return item.enabled && item.action !== 'Quick bet removal' && item.action !== 'Gaming cross sell removal';
  }
}