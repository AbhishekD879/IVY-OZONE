import { AbstractService } from './transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { Competition, CompetitionTab, CompetitionUpdate } from '../../models';
import { Order } from '../../models/order.model';

@Injectable()
export class CompetitionTabsService extends AbstractService<CompetitionTab> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = 'competitionTab';
  }

  createCompetitionTab(competitionId: string, competitionTab: CompetitionTab): Observable<HttpResponse<CompetitionTab>> {
    const uri = `competition/${competitionId}/tab`;
    return this.sendRequest<CompetitionTab>('post', uri, competitionTab);
  }

  getSingleCompetitionTab(competitionId: string, tabId: string): Observable<HttpResponse<Competition>> {
    const uri = `competition/${competitionId}/tab/${tabId}`;
    return this.sendRequest<Competition>('get', uri, null);
  }

  editCompetitionTab(updateData: CompetitionUpdate): Observable<HttpResponse<CompetitionTab>> {
    const uri = `${this.uri}/${updateData.id}`;
    return this.sendRequest<CompetitionTab>('put', uri, updateData);
  }

  deleteCompetitionTab(competitionId: string, id: string): Observable<HttpResponse<void>> {
    const uri = `competition/${competitionId}/tab/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }

  postNewTabsOrder(competitionId: string, order: Order): Observable<HttpResponse<CompetitionTab[]>> {
    const uri = `competition/${competitionId}/tab/ordering`;
    return this.sendRequest<CompetitionTab[]>('post', uri, order);
  }
}
