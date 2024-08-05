import { Component, Input, OnInit } from '@angular/core';
import environment from '@environment/oxygenEnvConfig';
import { ITeamAsset } from '@app/lazy-modules/fanzone/models/fanzone-team-asset.model';

@Component({
  selector: 'fanzone-crest-image',
  templateUrl: './fanzone-crest-image.component.html',
  styleUrls: ['./fanzone-crest-image.component.scss']
})
export class FanzoneCrestImageComponent implements OnInit {
  @Input() hasTeamImage: boolean = false;
  @Input() team: ITeamAsset;
  @Input() widthHeight: number;
  @Input() imgHeight?: number;
  @Input() fontWeight?: string;
  @Input() teamName: string;
  @Input() dialogText?: boolean = false;
  readonly CMS_UPLOADS_PATH: string = environment.CMS_ROOT_URI + environment.FIVEASIDE.svgImagePath;
  constructor() { }

  ngOnInit(): void { }

  /**
   * Method to check if team image or file name exists
   * @returns - true / false
   */
  checkForTeamsImageData(): boolean {
    return this.team && this.team.teamsImage && this.team.teamsImage.filename ? true : false;
  }
}
