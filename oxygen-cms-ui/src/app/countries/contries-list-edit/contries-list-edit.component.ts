import { Component, OnInit } from '@angular/core';
import { ApiClientService } from '../../client/private/services/http/index';
import { HttpResponse } from '@angular/common/http';
import { GlobalLoaderService } from '../../shared/globalLoader/loader.service';
import { Country } from '../../client/private/models/country.model';
import { DialogService } from '../../shared/dialog/dialog.service';
import { CountryCode } from '../../client/private/models/country.model';
import * as _ from 'lodash';
@Component({
  selector: 'app-contries-list-edit',
  templateUrl: './contries-list-edit.component.html',
  styleUrls: ['./contries-list-edit.component.scss'],
  providers: [
    DialogService
  ]
})
export class ContriesListEditComponent implements OnInit {

  public isLoading: boolean = false;
  public countries: Country;
  private allowedCountries: CountryCode[] = [];
  private bannedCountries: CountryCode[] = [];
  private initialActiveValues: Array<string>;
  private initialInActiveValues: Array<string>;

  constructor(
    private apiClientService: ApiClientService,
    private globalLoaderService: GlobalLoaderService,
    private dialogService: DialogService
  ) {
  }

  ngOnInit() {
   this.loadInitialData();
  }

  public saveChanges(): void {
    this.dialogService.showConfirmDialog({
      title: `Saving of Countries Setup`,
      message: `Are You Sure You Want to Save This Setup?`,
      yesCallback: () => {
        this.countries.countriesData = [];
        this.allowedCountries.forEach(country => {
          country.allowed = true;
          this.countries.countriesData.push(country);
        });
        this.bannedCountries.forEach(country => {
          country.allowed = false;
          this.countries.countriesData.push(country);
        });

        this.apiClientService.country()
            .edit(this.countries)
            .subscribe(() => {
              this.initialActiveValues = _.map(this.allowedCountries, 'val');
              this.initialInActiveValues = _.map(this.bannedCountries, 'val');
              this.dialogService.showNotificationDialog({
                title: `Countries Setup Saving`,
                message: `Countries Setup is Saved.`
              });
        });
      }
    });
  }

  public revertChanges(): void {
    this.loadInitialData();
  }

  public moveAllowedToBanned(): void {
    this.bannedCountries = this.bannedCountries.concat(this.allowedCountries);
    this.allowedCountries = [];
  }

  public moveBannedToAllowed(): void {
    this.allowedCountries = this.allowedCountries.concat(this.bannedCountries);
    this.bannedCountries = [];
  }

  public moveSelectedToBanned(): void {
    this.allowedCountries.forEach(country => {
      if (country.active) {
        this.bannedCountries.unshift(country);
      }
    });
    this.allowedCountries = this.allowedCountries.filter(country => !country.active);
    this.bannedCountries = this.bannedCountries.map((country) => {
      country.active = false;
      return country;
    });
  }

  public moveSelectedToAllowed(): void {
    this.bannedCountries.forEach(country => {
      if (country.active) {
        this.allowedCountries.unshift(country);
      }
    });
    this.bannedCountries = this.bannedCountries.filter(country => !country.active);
    this.allowedCountries = this.allowedCountries.map((country) => {
      country.active = false;
      return country;
    });
  }

  private showHideSpinner(toShow: boolean = true): void {
    toShow ? this.globalLoaderService.showLoader() : this.globalLoaderService.hideLoader();
    this.isLoading = toShow;
  }

  private loadInitialData(): void {
    this.showHideSpinner();
    this.apiClientService
        .country()
        .findAllByBrand()
        .map((coutryResponse: HttpResponse<Country[]>) => {
          return coutryResponse.body[0]; // ToDo: Check with BackEnd;
        })
        .subscribe((countries: Country) => {
          if (countries) {
            this.countries = countries;
            this.allowedCountries = this.countries.countriesData.filter(code => code.allowed);
            this.bannedCountries = this.countries.countriesData.filter(code => !code.allowed);
            this.initialActiveValues = _.map(this.allowedCountries, 'val');
            this.initialInActiveValues =  _.map(this.bannedCountries, 'val');
          }
          this.showHideSpinner(false);
        }, () => {
          this.showHideSpinner(false);
        });
  }

  public isButtonsDisabled(): boolean {
    return (this.initialActiveValues  === _.map(this.allowedCountries, 'val')) ||
           (this.initialInActiveValues === _.map(this.bannedCountries, 'val'));
  }
}
