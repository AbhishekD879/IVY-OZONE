import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Competition, CompetitionTab, CompetitionUpdate } from '../../models';
import { Order } from '../../models/order.model';

@Injectable()
export class CompetitionSubTabsService extends AbstractService<CompetitionTab> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'competitionSubTab';
  }

  createSubTab(competitionId: string, tabId: string, subTab: CompetitionTab): Observable<HttpResponse<CompetitionTab>> {
    const uri = `competition/${competitionId}/tab/${tabId}/subTab`;
    return this.sendRequest<CompetitionTab>('post', uri, subTab);
  }

  getSingleSubTab(competitionId: string, tabId: string, subTabId: string): Observable<HttpResponse<Competition>> {
    const uri = `competition/${competitionId}/tab/${tabId}/subTab/${subTabId}`;
    return this.sendRequest<Competition>('get', uri, null);
  }

  editSubTab(updateData: CompetitionUpdate): Observable<HttpResponse<CompetitionTab>> {
    const uri = `${this.uri}/${updateData.id}`;
    return this.sendRequest<CompetitionTab>('put', uri, updateData);
  }

  deleteSubTab(competitionId: string, tabId: string, id: string): Observable<HttpResponse<void>> {
    const uri = `competition/${competitionId}/tab/${tabId}/subTab/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  postNewSubTabsOrder(competitionId: string, tabId: string, order: Order): Observable<HttpResponse<CompetitionTab[]>> {
    const uri = `competition/${competitionId}/tab/${tabId}/subTab/ordering`;
    return this.sendRequest<CompetitionTab[]>('post', uri, order);
  }
}
