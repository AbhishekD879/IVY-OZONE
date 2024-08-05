import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {Competition, CompetitionModule, CompetitionUpdate} from '../../models';
import {Order} from '../../models/order.model';
import {KnockoutEventValid} from '../../models/knockouteventvalid.model';

@Injectable()
export class CompetitionModulesService extends AbstractService<CompetitionModule> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'competitionModule';
  }

  createCompetitionTabModule(competitionId: string, competitionTabId: string, competitionTabModule: CompetitionModule):
  Observable<HttpResponse<CompetitionModule>> {
    const uri = `competition/${competitionId}/tab/${competitionTabId}/module`;
    return this.sendRequest<CompetitionModule>('post', uri, competitionTabModule);
  }
  createCompetitionSubTabModule(competitionId: string, competitionTabId: string, subTabId: string,
                                competitionSubTabModule: CompetitionModule):
  Observable<HttpResponse<CompetitionModule>> {
    const uri = `competition/${competitionId}/tab/${competitionTabId}/subTab/${subTabId}/module`;
    return this.sendRequest<CompetitionModule>('post', uri, competitionSubTabModule);
  }

  postNewTabModulesOrder(competitionId: string, competitionTabId: string, order: Order):
  Observable<HttpResponse<CompetitionModule[]>> {
    const uri = `competition/${competitionId}/tab/${competitionTabId}/module/ordering`;
    return this.sendRequest<CompetitionModule[]>('post', uri, order);
  }

  postNewSubTabModulesOrder(competitionId: string, competitionTabId: string, subTabId: string, order: Order):
  Observable<HttpResponse<CompetitionModule[]>> {
    const uri = `competition/${competitionId}/tab/${competitionTabId}/subTab/${subTabId}/module/ordering`;
    return this.sendRequest<CompetitionModule[]>('post', uri, order);
  }

  getSingleModule(ids: string[]): Observable<HttpResponse<Competition>> {
    const isSubTabModule = ids.length > 3,
      url = isSubTabModule ? `subTab/${ids[2]}/module/${ids[3]}` : `module/${ids[2]}`;
    const uri = `competition/${ids[0]}/tab/${ids[1]}/${url}`;

    return this.sendRequest<Competition>('get', uri, null);
  }

  editModule(updateData: CompetitionUpdate): Observable<HttpResponse<CompetitionModule>> {
    const uri = `${this.uri}/${updateData.id}/${this.brand}`;
    return this.sendRequest<CompetitionModule>('put', uri, updateData);
  }

  deleteModule(ids: string[]): Observable<HttpResponse<void>> {
    const isSubTabModule = ids.length > 3,
      url = isSubTabModule ? `subTab/${ids[2]}/module/${ids[3]}` : `module/${ids[2]}`;
    const uri = `competition/${ids[0]}/tab/${ids[1]}/${url}`;

    return this.sendRequest<void>('delete', uri, null);
  }

  /**
   * Get market id and validate it
   * @param id
   * @returns {Observable<HttpResponse<any>>}
   */
  getSiteServeMarket(id: string): Observable<HttpResponse<any>> {
    const uri = `competition/brand/${this.brand}/ss/market/${id}`;
    return this.sendRequest<any>('get', uri, null);
  }

  /**
   * Get event id and validate it
   * @param id
   * @returns {Observable<HttpResponse<any>>}
   */
  getSiteServeEvent(id: number): Observable<HttpResponse<KnockoutEventValid>> {
    const uri = `competition/brand/${this.brand}/ss/knockout/event?eventId=${id}`;
    return this.sendRequest<any>('get', uri, null);
  }

  /**
   * Get statsCenter Competitions Groups
   * @param id
   * @returns {Observable<HttpResponse<any>>}
   */
  getCompetitionGroups(id: number): Observable<HttpResponse<any>> {
    const uri = `competition/${id}/stats/groups`;
    return this.sendRequest<any>('get', uri, null);
  }
}
