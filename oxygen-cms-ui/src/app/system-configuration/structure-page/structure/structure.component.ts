import {Component, OnInit} from '@angular/core';
import * as _ from 'lodash';

import {GlobalLoaderService} from '@app/shared/globalLoader/loader.service';
import {ConfigStructureAPIService} from '../service/structure.api.service';
import {IConfigData} from '../../config-page/models/IConfigData';
import {BrandService} from '@app/client/private/services/brand.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-structure',
  templateUrl: './structure.component.html',
  styleUrls: ['./structure.component.scss'],
  providers: [ConfigStructureAPIService]
})
export class StructureComponent implements OnInit {

  public _cmsData;
  public _filteredData = [];
  public _isLoading: boolean = true;
  public _searchField: string = '';

  constructor(
    private globalLoaderService: GlobalLoaderService,
    private configStructureAPIService: ConfigStructureAPIService,
    private brandService: BrandService,
    private route: ActivatedRoute
  ) {
  }

  ngOnInit() {
    this._searchField = (!this.route.snapshot.params.query) ? '' : this.route.snapshot.params.query;
    this.globalLoaderService.showLoader();
    this.configStructureAPIService.getStructureData()
      .map((data: any) => {
        if (data[1] && data[1].body.config) {
          data[1].body.config.sort((a, b) => {
            if (a.initialDataConfig === b.initialDataConfig) {
              return a.name < b.name ? -1 : 1;
            } else {
              return a.initialDataConfig ? -1 : 1;
            }
          });
        }
        return data;
      })
      .subscribe((data) => {
        this.globalLoaderService.hideLoader();
        this._isLoading = false;
        this._cmsData = this.applySystemConfigData(data);
      }, () => {
        this.globalLoaderService.hideLoader();
        this._isLoading = false;
      });
  }

  public get data() {
    if (this._searchField.length > 0) {
      return this._cmsData.filter((item) => {
        return ~item.name.toLowerCase().indexOf(this._searchField.toLowerCase());
      });
    } else {
      return this._cmsData;
    }
  }

  public saveButtonClickHandler() {
    const data = this._getSystemConfigObject();
    data.structure = this.filterIds(data.structure);
    this.configStructureAPIService.saveConfigStructure(data);
  }

  private _getSystemConfigObject() {
    return {
      lang: 'en',
      brand: this.brandService.brand,
      structure: _.reduce(this._cmsData, (result, value, key) => {
        /* tslint:disable */
        // Alejandro Del Rio Albrechet
        result[value.name] = _.reduce(value.items, (result, value, key) => {
          if (value.realMultiselectValueValue) {
            result[value.name] = {
              multiselectValue : this.transformMultiselectArrayToObject(value.realMultiselectValueValue),
              value : value.realValue
            };
          } else {
            result[value.name] = value.realValue;
          }
          return result;
        }, {});
        /* tslint:enable */
        return result;
      }, {})
    };
  }
  /**
   * Remove duplicate A-ZClassIDs and InitialClassIDs for sport competitions
   * @param  SystemConfigObject
   * @return {SystemConfigObject}
   */
  private filterIds(data) {
    const keys = Object.keys(data).filter((key) =>  key.toLowerCase().includes('competitions'));
    const filterData = (d) => [ ...new Set( d.replace(/ /g, '').split(','))].join();

    keys.forEach((key) => {
      ['A-ZClassIDs', 'InitialClassIDs'].forEach((prop) =>  data[key][prop] = data[key][prop] && filterData(data[key][prop]));

      // To remove duplicate ID`s from CMS UI
      const cmsItem = this._cmsData.find((item) => item.name === key);
      cmsItem.items.forEach((item) => {
        if (item.name === 'A-ZClassIDs' || item.name === 'InitialClassIDs') {
          item.realValue = filterData(item.realValue);
        }
      });
    });

    return data;
  }

  /**
   * Transfer data from configration structure to configuration data
   * @param {} data
   * @return {IConfigData} Config data with filled real data.
   */
  private applySystemConfigData(data: Array<any>): IConfigData {
    const systemConfig = data[0].body;
    const configuration = data[1].body.config;

    return configuration.map((configurationGroup) => {
      return this.applyConfigRealData(configurationGroup, systemConfig);
    });
  }

  /**
   * Transfer Structure data to group.
   * @param configurationGroup
   * @param systemConfig
   * @return {any}
   */
  applyConfigRealData(configurationGroup, systemConfig) {
    configurationGroup.items = configurationGroup.items ? configurationGroup.items.map((configurationGroupItem) => {
      return this.applyConfigItemRealData(configurationGroup.name, configurationGroupItem, systemConfig);
    }) : [];
    return configurationGroup;
  }

  /**
   * Transfer Structure data to group item.
   * @param configurationGroupName
   * @param configurationGroupItem
   * @param systemConfig
   * @return {any}
   */
  applyConfigItemRealData(configurationGroupName, configurationGroupItem, systemConfig) {
    const configItemRealValue = systemConfig[configurationGroupName][configurationGroupItem.name];
    const defaulValue = configurationGroupItem.value;

    if (configItemRealValue && configItemRealValue.multiselectValue && configItemRealValue.value) {
      configurationGroupItem.realValue = configItemRealValue.value;
      configurationGroupItem.realMultiselectValueValue = this.transformMultiselectObjectToArray(configItemRealValue.multiselectValue);
    } else {
      configurationGroupItem.realValue = _.isBoolean(configItemRealValue) ? configItemRealValue : configItemRealValue || defaulValue;
    }

    return configurationGroupItem;
  }

  /**
   * As we need array of items to create custom SelectBox,
   * we need to transform strange object to array
   * @param {} multiselectObject
   * @returns {string[]}
   */
  transformMultiselectObjectToArray(multiselectObject) {
    const multiselectArray = [];

    for (const item of Object.keys(multiselectObject)) {
      multiselectArray.push(multiselectObject[item]);
    }

    return multiselectArray;
  }

  /**
   * Backend used strange model and stores select optioons as object.
   * @param multiselectArray
   * @returns {{}}
   */
  transformMultiselectArrayToObject(multiselectArray) {
    const multiselectObject = {};

    multiselectArray.forEach((item, i) => {
      multiselectObject[i] = item;
    });

    return multiselectObject;
  }
}
