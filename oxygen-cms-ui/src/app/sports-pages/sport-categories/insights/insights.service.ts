import {Injectable} from '@angular/core';
import { Observable } from 'rxjs';
import { SportTab } from '@app/client/private/models/sporttab.model';
import { SportCategory } from '@app/client/private/models';
import { Order } from '@app/client/private/models/order.model';
import {HttpResponse } from '@angular/common/http';
import { ApiClientService } from '@root/app/client/private/services/http';

@Injectable()
export class InsightsService{
 

  constructor(private apiClientService:ApiClientService) {
   }
public getSportTabById(id: string): Observable<SportTab> {
    return this.apiClientService
      .sportTabService()
      .getById(id)
      .map((response: HttpResponse<SportTab>) => response.body);
  }

  public getSportCategoryById(id: string): Observable<SportCategory> {
    return this.apiClientService
      .sportCategory()
      .findOne(id)
      .map((data: HttpResponse<SportCategory>) => data.body);
  }

  public newOrder(newOrder: Order): Observable<any>  {
    return this.apiClientService.sportCategory().sportReorder(newOrder).map((data:any)=> data.body);
  }
}
