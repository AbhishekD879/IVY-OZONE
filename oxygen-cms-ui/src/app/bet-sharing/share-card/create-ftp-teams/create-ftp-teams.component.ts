import { Component,Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import * as _ from 'lodash';

@Component({
  selector: "app-create-ftp-teams",
  templateUrl: "./create-ftp-teams.component.html",
 })
export class CreateFtpTeamsComponent implements OnInit {
  teamPlayers: any = [];
  btnTitle: string = '';
  isValueChange: boolean;

  constructor(
    public dialogRef: MatDialogRef<CreateFtpTeamsComponent>,
    @Inject(MAT_DIALOG_DATA) public dialog: any
  ) {}

  ngOnInit(): void {
    if (this.dialog.title == "create") {
    this.teamPlayers = this.dialog.data.teamPlayers;
    this.formTeamPlayersObj( "", "");
    this.btnTitle = "Add Filter";
    }
    if (this.dialog.title == "edit") {
      const editData = this.dialog.data;
      this.formTeamPlayersObj(editData.teamName,editData.teamLogoUrl);
      this.btnTitle = "Edit Filter";
    }
  }

  /**
   * Filter popup form
   * @param name
   * @param url
   */
  public formTeamPlayersObj(name: string,url: string): void {
    this.teamPlayers = {
      teamName: name,
      teamLogoUrl: url,
    };
  }

  /**
   * cancel popup
   */
  public cancel(): void {
    this.dialogRef.close();
  }

  /**
   * popup filter values validaiton
   * @returns
   */
  public isValidTeamPlayersTable() {
    this.isValueChange = _.isEqual(this.teamPlayers, this.dialog.data);
    return !!(
      this.teamPlayers.teamName.length >0  &&  this.teamPlayers.teamName.length <=100 &&
      this.teamPlayers.teamLogoUrl.length >0 && this.teamPlayers.teamLogoUrl.length <= 100
    );
  }
}
