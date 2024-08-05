import { Component, OnInit, ViewChild } from '@angular/core';
import { BetShare, teamDetails } from '@app/client/private/models/betShare.model';
import { DialogService } from '../../shared/dialog/dialog.service';
import { Brand } from '@app/app.constants';
import { BrandService } from '@app/client/private/services/brand.service';
import { ApiClientService } from '@app/client/private/services/http';
import { ActionButtonsComponent } from '@app/shared/action-buttons/action-buttons.component';
import * as _ from 'lodash';
import { BET_SHARECARD_VALUES, FTPBETSHARING_CONFIG, FTP_BETSHARING_TEAMS_TABLE, LUCKYDIP_BETSHARINGCONFIG, LuckyDipUserPreferncesArray, UserPreferncesArray } from './bet-sharing-overlay.constants';
import {DataTableColumn} from '../../client/private/models'
import { AppConstants } from "@app/app.constants";
import { CreateFtpTeamsComponent } from './create-ftp-teams/create-ftp-teams.component';
import { CmsAlertComponent } from '@root/app/shared/cms-alert/cms-alert.component';
@Component({
  selector: 'app-share-card',
  templateUrl: './share-card.component.html',
  styleUrls: ['./share-card.component.scss']
})

export class ShareCardComponent implements OnInit {
  @ViewChild('actionButtons') actionButtons: ActionButtonsComponent;
  @ViewChild('requestError') private requestError: CmsAlertComponent;
  shareCardFormData: BetShare;
  limitExceeded: boolean;
  isBrandLads: boolean = false;
  openBetChecked: boolean = true;
  lostBetChecked: boolean = true;
  wonBetChecked: boolean = true;
  cashedOutBetChecked: boolean = true;
  ftpBetChecked:boolean = true;
  requestType: any;
  cashedOutBetControl: any;
  searchField: '';
  filterProperties: Array<string> = [
    'name'
  ];
  dataTableColumns: Array<DataTableColumn> = FTP_BETSHARING_TEAMS_TABLE;
  luckyDipOpenBetChecked: boolean = true;
  luckyDipWonBetChecked: boolean = true;
  luckyDipLostBetChecked: boolean = true;

  constructor(
    private apiService: ApiClientService,
    private dialogService: DialogService,
    private brandService: BrandService
  ) {

    this.verifyBetSharingData = this.verifyBetSharingData.bind(this);
  }

  ngOnInit(): void {
    this.isBrandLads = this.brandService.brand === Brand.LADBROKES;
    this.loadInitialData();
  }

  /**
    * To Load initial data
    */
  private loadInitialData(): void {
    this.apiService.betSharingApiService()
      .getDetailsByBrand()
      .subscribe((data: { body: BetShare }) => {
        if(!data.body){
          this.shareCardFormData = BET_SHARECARD_VALUES;
        } else {
        this.shareCardFormData = JSON.parse(JSON.stringify(data.body));
        if(!this.shareCardFormData.luckyDipBetSharingConfigs) {
        this.shareCardFormData.luckyDipBetSharingConfigs = {...LUCKYDIP_BETSHARINGCONFIG};
        }
        if(!this.shareCardFormData.ftpBetSharingConfigs) {
        this.shareCardFormData.ftpBetSharingConfigs = {...FTPBETSHARING_CONFIG};
        }
        }
        this.settingUserPrefernces();
        this.actionButtons?.extendCollection(this.shareCardFormData);
      }, error => {
        if (error.status === 404) {
          this.shareCardFormData = this.getDefaultValues();
        } else {
          this.dialogService.showNotificationDialog({
            title: 'Error occurred',
            message: (error?.error?.message) ? error?.error?.message : 'Ooops... Something went wrong, please contact support team'
          });
        }
      });
  }

  settingUserPrefernces() {
    const controls= ["openBetControl", "wonBetControl", "lostBetControl", "cashedOutBetControl"];
    controls.forEach((control) => {
      (control !== "cashedOutBetControl") && this.luckyDipAddCheckboxes(control);
      this.addCheckboxes(control);
    });
  }

  userPerferncesChange(control: string) {
    const data = this.shareCardFormData[control].some(x => x.isSelected === true);
    if (control === "openBetControl") {
      this.openBetChecked = data;
    } else if (control === "wonBetControl") {
      this.wonBetChecked = data;
    }
    else if (control === "lostBetControl") {
      this.lostBetChecked = data;
    }
    else if (control === "cashedOutBetControl") {
      this.cashedOutBetChecked = data;
    }
  }

  /**
   * changeUserPreferances for different Bet types like luckyDip, FTP
   * @param control 
   * To check uncheck the userpreferance for the specific object.
   */
  public changeBetUserPreference(event: any,index: number, control: string,type: string){
    this.shareCardFormData[type][control][index].isSelected = event.checked;
    const checked = this.shareCardFormData[type][control].some(x => x.isSelected === true);
    if(type.includes('luckyDip') && control.includes('openBet')) {
      this.luckyDipOpenBetChecked = checked;
    }
    else if(type.includes('luckyDip') && control.includes('wonBet')) {
      this.luckyDipWonBetChecked = checked;
    }
    else if(type.includes('luckyDip') && control.includes('lostBet')) {
      this.luckyDipLostBetChecked = checked;
    }
    else if(control.includes('ftp')){
      this.ftpBetChecked = checked;
    }
  }

  /**
    * To assign default values
    * @returns {BetShare}
    */
  private getDefaultValues(): BetShare {
    const popup = { ...BET_SHARECARD_VALUES };
    popup.brand = this.brandService.brand;
    return popup;
  }

  /**
   * To Handle actions
   * @param {string} event
   */
  actionsHandler(event: string): void {
    switch (event) {
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        break;
    }
  }

  /**
   * To save and edit
   * @param {string} requestType
   */
  saveChanges(): void {
    if (this.shareCardFormData.createdAt) {
      this.sendRequest('updateCMSBetShareData');
    } else {
      this.sendRequest('saveCMSBetShareData');
    }
  }

  /**
 * To save and edit
 * @param {string} requestType
 */
  private sendRequest(requestType: string, isInitialLoad: boolean = false): void {
    this.apiService.betSharingApiService()[requestType](this.shareCardFormData)
      .map((response) => response.body)
      .subscribe((data: BetShare) => {
        this.shareCardFormData = data;
        this.actionButtons?.extendCollection(this.shareCardFormData);
        if (!isInitialLoad) {
          this.dialogService.showNotificationDialog({
            title: 'Success',
            message: 'Your changes have been saved'
          });
        }
      }, error => {
        this.dialogService.showNotificationDialog({
          title: 'Error on saving',
          message: 'Ooops... Something went wrong, please contact support team'
        });
      });
  }

  revertChanges(): void {
    this.loadInitialData();
  }
/**
 * 
 * @param shareCardFormData 
 *  To validate the form data.
 * @returns boolean value
 */
  verifyBetSharingData(shareCardFormData: BetShare) {
    const isFormDataValid = !!(shareCardFormData && shareCardFormData.openBetShareCardMessage.length > 0 &&
      shareCardFormData.openBetShareCardSecondMessage.length > 0 && shareCardFormData.genericSharingLink.length > 0 && shareCardFormData.popUpDesc.length > 0 &&
      this.cashedOutBetChecked && this.openBetChecked && this.wonBetChecked && this.lostBetChecked && shareCardFormData.brandLogoUrl.length > 0
      && shareCardFormData.cashedOutBetsShareCardMessage.length > 0 && shareCardFormData.openBetsGenericUrl.length > 0
      && shareCardFormData.settledBetsGenericUrl.length > 0 && shareCardFormData.beGambleAwareLogoUrl.length > 0 && shareCardFormData.extensionUrl.length > 0
      && shareCardFormData.wonBetShareCardMessage.length > 0 && shareCardFormData.cashedOutBetsShareCardMessage.length > 0
      && this.luckyDipOpenBetChecked && this.luckyDipWonBetChecked && this.luckyDipLostBetChecked && shareCardFormData.luckyDipBetSharingConfigs.backgroundImageUrl.length >0 && shareCardFormData.luckyDipBetSharingConfigs.header.length >0 && shareCardFormData.luckyDipBetSharingConfigs.luckyDipAffiliateLink.length >0 
      && shareCardFormData.luckyDipBetSharingConfigs.potentialReturnsLabel
      && shareCardFormData.luckyDipBetSharingConfigs.luckyDipLabel.length >0 && shareCardFormData.luckyDipBetSharingConfigs.wonLabel.length >0
      && shareCardFormData.ftpBetSharingConfigs.teamDetails.length >0
      && shareCardFormData.ftpBetSharingConfigs.backgroundImageUrl.length >0 && shareCardFormData.ftpBetSharingConfigs.affiliateLink?.length >0 && shareCardFormData.ftpBetSharingConfigs.header.length >0
      && shareCardFormData.ftpBetSharingConfigs.playLabel?.length >0 && this.ftpBetChecked);
    return this.isBrandLads ? isFormDataValid &&  shareCardFormData.ftpBetSharingConfigs.subHeader.length >0 : isFormDataValid;
  }

  private luckyDipAddCheckboxes(control: string) {
    LuckyDipUserPreferncesArray.forEach((userPrefernce) => {
      const index = this.shareCardFormData.luckyDipBetSharingConfigs[control].findIndex((openBetData) => userPrefernce.name === openBetData.name);
      if (index < 0) {
        this.shareCardFormData.luckyDipBetSharingConfigs[control].push(userPrefernce);
      }
    });
    return this.shareCardFormData.luckyDipBetSharingConfigs[control];
  }

  private addCheckboxes(control) {
    UserPreferncesArray.forEach((userPrefernce) => {
      const index = this.shareCardFormData[control].findIndex((openBetData) => userPrefernce.name === openBetData.name);
      if (index < 0) {
        this.shareCardFormData[control].push(userPrefernce);
    }
    
    });
    return this.shareCardFormData[control];
  }

  /**
   * createFilter
   * To create the table with team and URL.
   */
  public createFilter(): void {
    this.dialogService.showCustomDialog(CreateFtpTeamsComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'create',
      yesOption: 'Save',
      noOption: 'Cancel', 
      data : this.shareCardFormData.ftpBetSharingConfigs.teamDetails,
      yesCallback: (filterItem): void => {
        let isDup : number; 
        isDup = this.shareCardFormData.ftpBetSharingConfigs.teamDetails.findIndex((item) => { 
          return (item.teamName === filterItem.teamName )
          }); 
          isDup >= 0 ?  this.requestError.showError(`Fliter with same properties exist!`): this.shareCardFormData.ftpBetSharingConfigs.teamDetails.push(filterItem);
       }
    });
  }

/**
 * editFilter
 * @param event having the specific object.
 *  To edits the specific row in Table.
 */
  public editFilter(event: teamDetails): void {
    const index = this.shareCardFormData.ftpBetSharingConfigs.teamDetails.indexOf(event);
    this.dialogService.showCustomDialog(CreateFtpTeamsComponent, {
      width: AppConstants.ADD_COMPONENT_MODAL_WINDOW_WIDTH,
      title: 'edit',
      yesOption: '',
      noOption: 'Cancel', 
      data : event,
      yesCallback: (filterItem): void => {
        let isDup : number; 
        isDup = this.shareCardFormData.ftpBetSharingConfigs.teamDetails.findIndex( teamDetail => (teamDetail.teamName === filterItem.teamName && teamDetail.teamLogoUrl === filterItem.teamLogoUrl));
          isDup >= 0 ?  this.requestError.showError(`Table with same properties exist!`):
          this.shareCardFormData.ftpBetSharingConfigs.teamDetails[index]=filterItem;
       }
    });
  }

/**
 * removeFilter
 * @param filterItem having specific object.
 *  To remove the spcific row from the table.
 */
  public removeFilter(filterItem: teamDetails): void {
    const removeMessage = 'Are You Sure You Want to Remove Filter ?';
    this.dialogService.showConfirmDialog({
      title: 'Remove',
      message: removeMessage,
      yesCallback: (): void => {
        const index = this.shareCardFormData.ftpBetSharingConfigs.teamDetails.indexOf(filterItem);
        this.shareCardFormData.ftpBetSharingConfigs.teamDetails.splice(index, 1);
      }
    });
  }
}
