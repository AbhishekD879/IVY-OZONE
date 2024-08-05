import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs/Observable';
import {TeamKit} from '@app/client/private/models/teamKit.model';
import {AbstractService} from '@app/client/private/services/http/transport/abstract.service';
import {Configuration} from '@app/client/private/models/configuration.model';

export class TeamKitService extends AbstractService<Configuration> {
  teamKitUrl: string = 'team-kit';
  teamKitByBrandUrl: string = `team-kit/brand/${this.brand}`;

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  public getTeamKits(): Observable<HttpResponse<TeamKit[]>> {
    return this.sendRequest<TeamKit[]>('get', this.teamKitByBrandUrl, null);
  }

  public getSingleTeamKit(id: string): Observable<HttpResponse<TeamKit>> {
    const url = `${this.teamKitUrl}/${id}`;
    return this.sendRequest<TeamKit>('get', url, null);
  }

  public postNewTeamKit(game: TeamKit): Observable<HttpResponse<TeamKit>> {
    return this.sendRequest<TeamKit>('post', this.teamKitUrl, game);
  }

  public putTeamKitChanges(id: string, game: TeamKit): Observable<HttpResponse<TeamKit>> {
    const apiUrl = `${this.teamKitUrl}/${id}`;
    return this.sendRequest<TeamKit>('put', apiUrl, game);
  }

  public deleteTeamKit(id: string): Observable<HttpResponse<void>> {
    const url = `${this.teamKitUrl}/${id}`;
    return this.sendRequest<void>('delete', url, null);
  }

  public getTeamKitByName(teamName: string): Observable<HttpResponse<TeamKit[]>> {
    const url = `${this.teamKitByBrandUrl}/${teamName}`;
    return this.sendRequest<TeamKit[]>('get', url, null);
  }
}
