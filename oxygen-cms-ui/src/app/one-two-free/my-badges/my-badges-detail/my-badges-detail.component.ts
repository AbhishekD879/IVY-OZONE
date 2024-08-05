import {  ChangeDetectorRef, Component, OnInit, ViewChild } from '@angular/core';
import { DialogService } from '@root/app/shared/dialog/dialog.service';
import { MyBadges } from '@root/app/one-two-free/constants/otf.model';
import { MybadgesApiService } from '@root/app/one-two-free/service/mybadges.api.service';

@Component({
  selector: 'app-my-badges-detail',
  templateUrl: './my-badges-detail.component.html',
  styleUrls: ['./my-badges-detail.component.scss']
})
export class MyBadgesDetailComponent implements OnInit{
  constructor(private myBadgeService: MybadgesApiService,
    private dialogService: DialogService,private cdr: ChangeDetectorRef,) { }
  myBadges = new MyBadges();
  @ViewChild('actionButtons') actionButtons;
  isUpdate: boolean = false;
  dataLoaded: boolean = false;
  errors = {
    required: 'This Field is required*'
  }

  ngOnInit(): void {
    this.loadMybadgeData();
  }

  /**
   * Method to make a get call for fetching saved badge data
   *  @param: null
   * @returns void
   */
  loadMybadgeData(): void {
    this.myBadgeService.getMyBadgesData().subscribe(data => {
      this.myBadges = data.body;
      this.dataLoaded = true;
    }, (err) => {
      console.error(err);
    })
  }

  /**
   * Method to create or updated My badge data 
   *  @param: null
   */
  createEditbadges() {
    /* Create Flow */
    if (!this.myBadges.id) {
      this.myBadgeService.createMyBadges(this.myBadges).subscribe(data => {
        this.successDialog('Created');
        this.myBadges = data.body;
      })
    } else {
      /* Update Flow */
      this.myBadgeService.updateMyBadges(this.myBadges).subscribe(data => {
        this.myBadges = data.body;
        this.actionButtons.extendCollection(this.myBadges);
        this.successDialog('Updated');
      })
    }
  }

  /**
  * Confirmation dialog on successful creation or updation of My Badges data
  *  @param: type
  */
  successDialog(type: string) {
    this.dialogService.showNotificationDialog({
      title: 'My Badges',
      message: 'My badges ' + type + ' Succesfully!! '
    });
  }

  /**
  * Action Handler for Action buttons 
  *  @param: event
  */
  actionsHandler(event) {
    switch (event) {
      case 'save':
        this.createEditbadges();
        break;
      case 'revert':
        this.loadMybadgeData();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  /**
   * validation for action buttons (save)
   *  @param: myBadges
   */
  isValidModel(myBadges : MyBadges) {
    return myBadges.label &&
      myBadges.label.length > 0 &&
      !(myBadges.label.length > 50) &&
      myBadges.rulesDisplay &&
      myBadges.rulesDisplay.length > 0 &&
      !(myBadges.rulesDisplay.length > 250) &&
      myBadges.viewButtonLabel &&
      myBadges.viewButtonLabel.length > 0 &&
      !(myBadges.viewButtonLabel.length > 50) &&
      myBadges.lbrRedirectionLabel &&
      myBadges.lbrRedirectionLabel.length > 0 &&
      !(myBadges.lbrRedirectionLabel.length > 50) &&
      myBadges.lbrRedirectionUrl &&
      myBadges.lbrRedirectionUrl.length > 0
  }

  /**
   *Validation to show action button post form initialization
   *  @param: null
   */
  isLoadBadges() {
    return Object.keys(this.myBadges).length > 0;
  }
  /**
   *to update output data of tinymce editor 
   *  @param: data
   */
  updateRules(data : string) {
    const rulesHtml = document.createElement('div');
    rulesHtml.innerHTML = data;
    this.myBadges.rulesDisplay = rulesHtml.innerText;
    this.cdr.detectChanges();
  }
}
