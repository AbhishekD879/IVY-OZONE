import { Injectable } from '@angular/core';
import { onboardImageDataModel, OnboardModel } from '@root/app/betpack-market-place/model/bet-pack-banner.model';

@Injectable({
  providedIn: 'root'
})
export class BetpackOnboardService {

  onboardBetpack: Array<OnboardModel> = []
  totalOnboardImageData: onboardImageDataModel;
  editCreateOnboardData: Array<OnboardModel> = [];
  constructor() { }

  /**
   * set create and edit onboard data
   * @param onboardData 
   */
  setOnboardData(onboardData) {
    let index = this.onboardBetpack.findIndex(image => image.id == onboardData.id);
    if (index >= 0) {
      this.onboardBetpack.splice(index, 1);
      this.onboardBetpack.push(onboardData);
    }
    else {
      this.onboardBetpack.push(onboardData);
    }
  }

  /**
   * set updated onbord data
   * @param updateOnboardData 
   */
  setUpdateOnboardData(updateOnboardData) {
    this.onboardBetpack = []
    this.onboardBetpack = updateOnboardData;
  }

  /**
   * get create and edit onboard data
   * @returns {OnboardModel}
   */
  getOnboardData() {
    return this.onboardBetpack;
  }

  /**
   * set empty data
   * @param emptyOnboard 
   */
  setEmpty(emptyOnboard) {
    this.onboardBetpack = []
  }

  /**
   * create new onboard data
   * @param newOnboardData 
   */
  setCreateOnboardData(newOnboardData) {
    this.editCreateOnboardData = newOnboardData;
  }

  /**
   * get create new onboard data
   * @returns {OnboardModel}
   */
  getCreateOnboardData() {
    return this.editCreateOnboardData
  }

  /**
   * send edit onboardData
   * @param totalData 
   * @returns {onboardImageDataModel}
   */
  sendEditRequest(totalData) {
    this.totalOnboardImageData = totalData;
    return this.totalOnboardImageData;
  }

  /**
   * get edit onboardData
   * @returns {onboardImageDataModel}
   */
  getOnboardEditData() {
    return this.totalOnboardImageData;
  }
}
