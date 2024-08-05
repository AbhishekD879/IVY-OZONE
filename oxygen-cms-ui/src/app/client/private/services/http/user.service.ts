import {AbstractService} from './transport/abstract.service';
import {User} from '../../models/user.model';
import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import { Observable} from 'rxjs';

@Injectable()
export class UserService extends AbstractService<User> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `user`;
  }

  public retrieveAllUsers(): Observable<HttpResponse<User[]>> {
    return this.findAll();
  }

  public searchesUserById(id: string): Observable<HttpResponse<User>> {
    return this.findById(id);
  }

  public deleteUser(id: string): Observable<HttpResponse<any>> {
    return this.delete(id);
  }

  public createUser(user: User): Observable<HttpResponse<User>> {
    return this.sendRequest<any>('post', this.uri, user);
  }

  public updateUser(user: User): Observable<HttpResponse<User>> {
    this.uri = `user/${user.id}`;
    return this.sendRequest<any>('put', this.uri, user);
  }
}