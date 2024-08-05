import {Injectable} from '@angular/core';
import {HttpErrorResponse, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import 'rxjs/add/operator/catch';
import 'rxjs/add/observable/throw';
import * as _ from 'lodash';

import {GlobalLoaderService} from '../../../shared/globalLoader/loader.service';
import {ApiClientService} from '../../../client/private/services/http/index';
import {
  Competition,
  CompetitionModule,
  CompetitionParticipant,
  CompetitionParticipantUpdate,
  CompetitionTab,
  CompetitionUpdate,
  OBEvents,
  StatsCenterGroups
} from '../../../client/private/models';
import {KnockoutEventValid} from '../../../client/private/models/knockouteventvalid.model';
import {Order} from '../../../client/private/models/order.model';

@Injectable()
export class BigCompetitionAPIService {
  constructor(
    private globalLoaderService: GlobalLoaderService,
    private apiClientService: ApiClientService) {
  }

  /**
   * Wrap request to handle success/error.
   * @param {Observable<HttpResponse>} observableDate
   */
  wrappedObservable(observableDate: Observable<HttpResponse<any>>) {
    return observableDate
      .map(res => {
        this.globalLoaderService.hideLoader();
        return res;
      })
      .catch(response => {
        if (response instanceof HttpErrorResponse) {
          const message = response.error ? response.error.message : response.message;
          this.handleRequestError(message);
        }

        return Observable.throw(response);
      });
  }

  /**
   * Handle networking error.
   * Notify user.
   * @param {string} message
   */
  handleRequestError(message: string) {
    this.globalLoaderService.hideLoader();
  }

  // Competitions API
  /**
   * Get competitions data.
   * @returns {Observable<HttpResponse<Competition[]>>}
   */
  getCompetitionsList() {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitions().findAllCompetitions();

    return this.wrappedObservable(getData);
  }

  getCompetitionsListInByb(){
    this.globalLoaderService.showLoader();
    const getData = this.apiClientService.competitions().findAllCompetitions();
    return this.wrappedObservable(getData)
  }

  /**
   * Load single competition data to edit.
   * @param {string} id
   * @returns {any}
   */
  getSingleCompetition(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitions().getSingleCompetition(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to competition.
   * @param {CompetitionUpdate} competition
   */
  putCompetitionChanges(competition: CompetitionUpdate) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitions().editCompetition(competition);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes competition.
   * @param {string} id
   */
  deleteCompetition(id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitions().deleteCompetition(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new competition.
   * @param {Competition} competition
   */
  createCompetition(competition: Competition) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitions().createCompetition(competition);
    return this.wrappedObservable(getData);
  }

  // Competition Tabs API
  /**
   * Load single competition tab data to edit.
   * @param {string} competitionId
   * @param {string} tabId
   * @returns {any}
   */
  getSingleCompetitionTab(competitionId: string, tabId: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionTabs().getSingleCompetitionTab(competitionId, tabId);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to competitionTab.
   * @param {CompetitionUpdate} competitionTab
   */
  putCompetitionTabChanges(competitionTab: CompetitionUpdate) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionTabs().editCompetitionTab(competitionTab);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes competitionTab.
   * @param {string} competitionId
   * @param {string} id
   */
  deleteCompetitionTab(competitionId: string, id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionTabs().deleteCompetitionTab(competitionId, id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new competitionTab.
   * @param {string} competitionId
   * @param {CompetitionTab} competitionTab
   */
  createCompetitionTab(competitionId: string, competitionTab: CompetitionTab) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionTabs().createCompetitionTab(competitionId, competitionTab);
    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for tabs in competition.
   * @param {string} competitionId
   * @param {Order} order
   * @returns {Observable<HttpResponse<CompetitionTab[]>>}
   */
  postNewTabsOrder(competitionId: string, order: Order) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionTabs().postNewTabsOrder(competitionId, order);

    return this.wrappedObservable(getData);
  }

  // Competition Sub-Tabs API
  /**
   * Load single competition tab data to edit.
   * @param {string} competitionId
   * @param {string} tabId
   * @param {string} subTabId
   * @returns {any}
   */
  getSingleSubTab(competitionId: string, tabId: string, subTabId: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionSubTabs().getSingleSubTab(competitionId, tabId, subTabId);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to sub tab.
   * @param {CompetitionUpdate} subTab
   */
  putSubTabChanges(subTab: CompetitionUpdate) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionSubTabs().editSubTab(subTab);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes sub tab.
   * @param {string} competitionId
   * @param {string} tabId
   * @param {string} id
   */
  deleteSubTab(competitionId: string, tabId: string, id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionSubTabs().deleteSubTab(competitionId, tabId, id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new sub tab.
   * @param {string} competitionId
   * @param {string} tabId
   * @param {CompetitionTab} competitionTab
   */
  createSubTab(competitionId: string, tabId: string, competitionTab: CompetitionTab) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionSubTabs().createSubTab(competitionId, tabId, competitionTab);
    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for sub tabs in competition.
   * @param {string} competitionId
   * @param {string} tabId
   * @param {any} order
   * @returns {Observable<HttpResponse<CompetitionTab[]>>}
   */
  postNewSubTabsOrder(competitionId: string, tabId: string, order: any) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionSubTabs().postNewSubTabsOrder(competitionId, tabId, order);

    return this.wrappedObservable(getData);
  }

  // Competition Module API
  /**
   * Create new module
   * @param {string} competitionId
   * @param {string} tabId
   * @param {Object<CompetitionModule>} competitionModule
   * @returns {Observable<HttpResponse<CompetitionModule[]>>}
   */
  createTabModule(competitionId: string, tabId: string, competitionModule: CompetitionModule): Observable<HttpResponse<CompetitionModule>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().createCompetitionTabModule(competitionId, tabId, competitionModule);
    return this.wrappedObservable(getData);
  }

  /**
   * Create new module
   * @param {string} competitionId
   * @param {string} tabId
   * @param {string} subTabId
   * @param {Object<CompetitionModule>} competitionModule
   * @returns {Observable<HttpResponse<CompetitionModule[]>>}
   */
  createSubTabModule(competitionId: string, tabId: string, subTabId: string, competitionModule: CompetitionModule):
  Observable<HttpResponse<CompetitionModule>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().createCompetitionSubTabModule(competitionId, tabId,
      subTabId, competitionModule);
    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for module in competition tab.
   * @param {string} competitionId
   * param {string} competitionTabId
   * @param {any} order
   * @returns {Observable<HttpResponse<CompetitionModule[]>>}
   */
  postNewTabModulesOrder(competitionId: string, competitionTabId: string, order: any):
  Observable<HttpResponse<CompetitionModule>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().postNewTabModulesOrder(competitionId,
      competitionTabId, order);

    return this.wrappedObservable(getData);
  }

  /**
   * Posts new order for module in competition sub tab.
   * @param {string} competitionId
   * @param {string} competitionTabId
   * @param {string} subTabId
   * @param {any} order
   * @returns {Observable<HttpResponse<CompetitionModule[]>>}
   */
  postNewSubTabModulesOrder(competitionId: string, competitionTabId: string, subTabId: string, order: any):
  Observable<HttpResponse<CompetitionModule>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().postNewSubTabModulesOrder(competitionId,
      competitionTabId, subTabId, order);

    return this.wrappedObservable(getData);
  }

  /**
   * Load single competition module data to edit.
   * @param args
   * @returns {Observable<HttpResponse<Competition>>}
   */
  getSingleModule(...args): Observable<HttpResponse<Competition>> {
    const ids = _.compact(args);
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().getSingleModule(ids);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to module.
   * @param {module} module
   * @returns {Observable<HttpResponse<CompetitionModule>>}
   */
  putModuleChanges(module: any): Observable<HttpResponse<CompetitionModule>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().editModule(module);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes module.
   * @param args
   * @returns {Observable<HttpResponse<void>>}
   */
  deleteModule(...args): Observable<HttpResponse<void>> {
    const ids = _.compact(args);
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().deleteModule(ids);
    return this.wrappedObservable(getData);
  }

  // Competition Participants API
  /**
   * Load single competition participant data to edit.
   * @param {string} competitionId
   * @param {string} participantId
   * @returns {Observable<HttpResponse<CompetitionParticipant>>}
   */
  getSingleParticipant(competitionId: string, participantId: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionParticipants().getSingleParticipant(competitionId, participantId);
    return this.wrappedObservable(getData);
  }

  /**
   * Puts changes to participant.
   * @param {Object} participant update data
   * @returns {Observable<HttpResponse<CompetitionParticipant>>}
   */
  putParticipantChanges(participant: CompetitionParticipantUpdate) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionParticipants().editParticipant(participant);
    return this.wrappedObservable(getData);
  }

  /**
   * Deletes participant.
   * @param {string} participantId
   * @param {string} id
   */
  deleteParticipant(participantId: string, id: string) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionParticipants().deleteParticipant(participantId, id);
    return this.wrappedObservable(getData);
  }

  /**
   * Creates new participant.
   * @param {string} competitionId
   * @param {Object} participant
   * @returns {Observable<HttpResponse<CompetitionParticipant>>}
   */
  createParticipant(competitionId: string, participant: CompetitionParticipantUpdate) {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionParticipants().createParticipant(competitionId, participant);
    return this.wrappedObservable(getData);
  }

  /**
   * Uploads svg icon for given participant.
   * @param {string} participantId
   * @param {Object} file
   * @returns {Observable<HttpResponse<CompetitionParticipant>>}
   */
  uploadParticipantSvg(participantId: string, file: FormData): Observable<HttpResponse<CompetitionParticipant>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionParticipants().uploadSvg(participantId, file);
    return this.wrappedObservable(getData);
  }

  /**
   * Removes svg icon for given participant.
   * @param {string} participantId
   * @returns {Observable<HttpResponse<CompetitionParticipant>>}
   */
  removeParticipantSvg(participantId: string): Observable<HttpResponse<CompetitionParticipant>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionParticipants().removeSvg(participantId);
    return this.wrappedObservable(getData);
  }


  /**
   * Get market id and validate
   * @param id
   * @returns {Observable<HttpResponse><any>}
   */
  getSiteServeMarket(id: string): Observable<HttpResponse<any>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().getSiteServeMarket(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Get event id and validate
   * @param id
   * @returns {Observable<HttpResponse><any>}
   */
  getSiteServeEvent(id: number): Observable<HttpResponse<KnockoutEventValid>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().getSiteServeEvent(id);
    return this.wrappedObservable(getData);
  }

  /**
   * Get statsCenter Competitions Groups
   * @param compId - competition ID
   * @returns {Observable<HttpResponse><any>}
   */
  getCompetitionGroups(compId: number): Observable<HttpResponse<StatsCenterGroups>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitionModules().getCompetitionGroups(compId);
    return this.wrappedObservable(getData);
  }

  /**
   * Load site serve events by ids.
   * @param options
   * @returns {Observable<HttpResponse<OBEvents>>}
   */
  getSiteServeEvents(options): Observable<HttpResponse<OBEvents>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitions().getSiteServeEvents(options);
    return this.wrappedObservable(getData);
  }

  getSiteServeEventsByType(options): Observable<HttpResponse<OBEvents>> {
    this.globalLoaderService.showLoader();

    const getData = this.apiClientService.competitions().getSiteServeEventsByType(options);
    return this.wrappedObservable(getData);
  }
}
