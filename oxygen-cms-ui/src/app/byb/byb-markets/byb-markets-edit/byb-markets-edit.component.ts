import * as _ from 'lodash';

import { Component, OnInit, ViewChild } from '@angular/core';
import { HttpResponse } from '@angular/common/http';
import { Router, ActivatedRoute, Params } from '@angular/router';

import { DialogService } from '../../../shared/dialog/dialog.service';
import { BybAPIService } from '../../service/byb.api.service';
import { BybMarket } from '../../../client/private/models';
import { Breadcrumb } from '../../../client/private/models/breadcrumb.model';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'byb-markets-edit',
  templateUrl: './byb-markets-edit.component.html',
  styleUrls: ['./byb-markets-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class BybMarketsEditComponent implements OnInit {

  public bybMarket: BybMarket;
  public form: FormGroup;
  @ViewChild('actionButtons') actionButtons;
  public breadcrumbsData: Breadcrumb[];
  market_type: Array<string> = ['N/A', 'Player Bet', 'Team Bet'];
  stat_type: Array<string> = ['Passes', 'Tackles', 'Shots', 'Shots On Target', 'Shots Outside The Box', 'Assists', 'Offsides', 'Goals Inside The Box', 'Goals Outside The Box', 'Shots Against The Woodwork', 'Cards', 'Goals', 'To Be Shown A Card', 'Goalscorer'];

  constructor(
    private bybAPIService: BybAPIService,
    private activatedRoute: ActivatedRoute,
    private dialogService: DialogService,
    private router: Router
  ) { }

  ngOnInit() {
    this.loadInitData();
  }

  saveChanges(): void {
    _.extend(this.bybMarket, this.getBybMarket());
    this.bybAPIService
      .putMarketChanges(this.bybMarket)
      .map((bybMarket: HttpResponse<BybMarket>) => {
        return bybMarket.body;
      })
      .subscribe((data: BybMarket) => {
        this.bybMarket = data;
        this.actionButtons.extendCollection(this.getBybMarket());
        this.dialogService.showNotificationDialog({
          title: `BuildYourBet Market`,
          message: `BuildYourBet Market is Saved`
        });
      });
  }

  revertChanges(): void {
    this.loadInitData();
  }

  removeBybMarket(): void {
    this.bybAPIService.deleteMarket(this.bybMarket.id)
      .subscribe(() => {
        this.router.navigate(['/byb/byb-markets']);
      });
  }

  public actionsHandler(event): void {
    switch (event) {
      case 'remove':
        this.removeBybMarket();
        break;
      case 'save':
        this.saveChanges();
        break;
      case 'revert':
        this.revertChanges();
        break;
      default:
        console.error('Unhandled Action');
        break;
    }
  }

  private loadInitData(): void {
    this.activatedRoute.params.subscribe((params: Params) => {
      this.bybAPIService.getSingleMarket(params['id'])
        .map((bybMarket: HttpResponse<BybMarket>) => {
          return bybMarket.body;
        })
        .subscribe((bybMarket: BybMarket) => {
          this.bybMarket = bybMarket;
          this.form = new FormGroup({
            name: new FormControl(this.bybMarket.name, [
              Validators.required
            ]),
            bybMarket: new FormControl(this.bybMarket.bybMarket, [
              Validators.required
            ]),
            incidentGrouping: new FormControl(this.bybMarket.incidentGrouping, [
              Validators.pattern('^\\d+$')
            ]),
            marketGrouping: new FormControl(this.bybMarket.marketGrouping, [
              Validators.pattern('^\\d+$')
            ]),
            stat: new FormControl(this.bybMarket.stat, []),
            marketType: new FormControl(this.bybMarket.marketType, []),
            popularMarket: new FormControl(this.bybMarket.popularMarket, []),
            marketDescription: new FormControl(this.bybMarket.marketDescription, [])
          });
          this.breadcrumbsData = [{
            label: `Build Yout Bet Markets`,
            url: `/byb/byb-markets`
          }, {
            label: this.bybMarket.name,
            url: `/byb/byb-markets/${this.bybMarket.id}`
          }];
        });
    });
  }

  setStat(event): void {
    if (event !== 'Player Bet') {
      this.form.controls.stat.setValidators([]);
      this.form.controls.stat.setValue('');
    }
  }

  public getBybMarket(): BybMarket {
    return this.form.value;
  }

  public get name(): AbstractControl {
    return this.form.get('name');
  }

  public get marketGroupName(): AbstractControl {
    return this.form.get('bybMarket');
  }

  public get incidentGrouping(): AbstractControl {
    return this.form.get('incidentGrouping');
  }

  public get marketGrouping(): AbstractControl {
    return this.form.get('marketGrouping');
  }

  public get stat(): AbstractControl {
    return this.form.get('stat');
  }

  public get marketType(): AbstractControl {
    return this.form.get('marketType');
  }

  public get popularMarket(): AbstractControl {
    return this.form.get('popularMarket');
  }

  public get marketDescription(): AbstractControl {
    return this.form.get('marketDescription');
  }
}

