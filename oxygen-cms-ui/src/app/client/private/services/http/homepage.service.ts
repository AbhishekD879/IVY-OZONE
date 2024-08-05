import {Configuration} from '../../models/configuration.model';
import {AbstractService} from './transport/abstract.service';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {SportsModule} from '../../models/homepage.model';
import {Order} from '../../models/order.model';
import { HomeInplayModule, InplaySports } from '../../models/inplaySportModule.model';
@Injectable()
export class HomepageService extends AbstractService<Configuration> {
  homepageUrl: string = 'homepage';
  sportsModulesUrl: string = 'sport-module';
  sportsInplayModuleUrl: string = 'home-inplay-sport';

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getAllModules(): Observable<HttpResponse<SportsModule[]>> {
    return this.sendRequest<SportsModule[]>('get', `${this.sportsModulesUrl}`, null);
  }

  /**
   * @param pageType - 'sport' or 'eventhub'
   * @param pageId - sport id or eventhub index
   */
  public getAllModulesBySport(pageType: string, pageId: number): Observable<HttpResponse<SportsModule[]>> {
    const url = `${this.sportsModulesUrl}/brand/${this.brand}/${pageType}/${pageId}`;

    return this.sendRequest<SportsModule[]>('get', url, null);
  }

  public getModuleById(moduleId: string): Observable<HttpResponse<SportsModule>> {
    return this.sendRequest<SportsModule>('get', `${this.sportsModulesUrl}/${moduleId}`, null);
  }

  public postNewModule(module: SportsModule): Observable<SportsModule> {
    module.brand = this.brand;

    return this.sendRequest<SportsModule>('post', this.sportsModulesUrl, module)
      .map(response => response.body);
  }

  public updateModule(module: SportsModule): Observable<SportsModule> {
    return this.sendRequest<SportsModule>('put', `${this.sportsModulesUrl}/${module.id}`, module)
      .map(response => response.body);
  }

  public removeModule(moduleId: string): Observable<SportsModule> {
    return this.sendRequest<SportsModule>('delete', `${this.sportsModulesUrl}/${moduleId}`, null)
      .map(response => response.body);
  }

  public reorder(obj: Order): Observable<HttpResponse<SportsModule[]>> {
    const uri = `${this.sportsModulesUrl}/ordering`;
    return this.sendRequest<SportsModule[]>('post', uri, obj);
  }

  public getInplaySportsBySegment(segment: string, brand: string): Observable<HomeInplayModule[]> {
    const uri = `${this.sportsInplayModuleUrl}/brand/${brand}/segment/${segment}`;
    return this.sendRequest<HomeInplayModule[]>('get', uri, null)
    .map(response => response.body);
  }

  public getAllSportNames(): Observable<InplaySports[]> {
    const uri = `sport-category/sport-name/brand/${this.brand}`;
    return this.sendRequest<InplaySports[]>('get', uri, null)
    .map(response => response.body);
  }

  public getInplaySportById(id: string): Observable<HomeInplayModule> {
    const uri = `${this.sportsInplayModuleUrl}/${id}`;
    return this.sendRequest<HomeInplayModule>('get', uri, null)
    .map(response => response.body);
  }

  public saveNewInplaySport(newInplaySport: HomeInplayModule): Observable<HomeInplayModule> {
    const uri = `${this.sportsInplayModuleUrl}`;
    return this.sendRequest<HomeInplayModule>('post', uri, newInplaySport)
    .map(response => response.body);
  }

  public deleteSportById(id: string): Observable<HomeInplayModule> {
    const uri = `${this.sportsInplayModuleUrl}/${id}`;
    return this.sendRequest<HomeInplayModule>('delete', uri, null)
    .map(response => response.body);
  }

  public updateNewInplaySport(newInplaySport: HomeInplayModule): Observable<HomeInplayModule> {
    const uri = `${this.sportsInplayModuleUrl}/${newInplaySport.id}`;
    return this.sendRequest<HomeInplayModule>('put', uri, newInplaySport)
    .map(response => response.body);
  }

  public inplaySportsReorder(obj: Order): Observable<HttpResponse<HomeInplayModule[]>> {
    const uri = `${this.sportsInplayModuleUrl}/ordering`;
    return this.sendRequest<HomeInplayModule[]>('post', uri, obj);
  }
}
