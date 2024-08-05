import { AbstractService } from '@app/client/private/services/http/transport/abstract.service';
import { Injectable } from '@angular/core';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { NavigationGroup, NavTypeContent, PromoNavContent, PromoNavItems, PromotionNavigation, PromotionsNavigationGroup } from '@app/client/private/models/promotions-navigation.model';
import { Order } from '@app/client/private/models/order.model';

@Injectable()
export class PromotionsNavigationsService extends AbstractService<any[]> {
  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
    this.uri = `navigation-group`;

  }
  navItemUri = `nav-item/navigation-groupId`;
  navItem = `nav-item`;

  /**
   * Get All Nav Groups by brand.
   * @param {} 
   * @returns {Observable<HttpResponse<PromotionsNavigationGroup[]>>}
   */
  public findAllByBrand(): Observable<HttpResponse<PromotionsNavigationGroup[]>> {
    return this.sendRequest<PromotionsNavigationGroup[]>('get', `${this.uri}/brand/${this.brand}`, null);
  }

  /**
   * remove Nav Parent Group.
   * @param {string} id
   * @param {string[]} promotionIds
   * @returns {Observable<HttpResponse<void>>}
   */
  public remove(id: string, promotionIds: `""` | string[]): Observable<HttpResponse<void>> {
    const uri = `${this.uri}/${id}/${promotionIds}`;
    return this.sendRequest<void>('delete', uri, null);
  }


  /**
 * Posts new  Nav Parent Group.
 * @param {navigationGroup} NavigationGroup
 * @returns {Observable<HttpResponse<PromotionNavigation>>}
 */
  public add(navigationGroup: NavigationGroup): Observable<HttpResponse<PromotionNavigation>> {
    return this.sendRequest<PromotionNavigation>('post', this.uri, navigationGroup);
  }

  /**
 * Update Nav Parent Group.
  * @param {navigationGroup} NavigationGroup
 * @returns {Observable<HttpResponse<PromotionNavigation>>}
 */
  public updateNavGroup(navigationGroup: any): Observable<HttpResponse<PromotionsNavigationGroup>> {
    navigationGroup.brand = this.brand;
    const uri = `${this.uri}/${navigationGroup.id}`;
    return this.sendRequest<PromotionsNavigationGroup>('put', uri, navigationGroup);
  }

  /**
* Posts new order for Nav Parent Group.
* @param {any} order
* @returns {Observable<HttpResponse<void>>}
*/
  public postNewPromotionsNavigationsOrder(order: Order): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('post', `${this.uri}/ordering`, order);
  }

  /**
* get Nav List by ID
* @param {id} string
* @returns {Observable<HttpResponse<PromotionsNavigationGroup>>}
*/
  public getNavListById(id: string): Observable<HttpResponse<PromotionsNavigationGroup>>  {
    const uri = `${this.navItemUri}/${id}`;
    return this.sendRequest<PromotionsNavigationGroup>('get', uri, null);
  }

  /**
 * Posts new  Nav Item.
 * @param {navContent} NavTypeContent
 * @returns {Observable<HttpResponse<PromoNavContent>>}
 */
  public postNavContent(navContent: NavTypeContent): Observable<HttpResponse<PromoNavContent>> {
    navContent.brand = `${this.brand}`;
    return this.sendRequest<PromoNavContent>('post', this.navItem, navContent);
  }


  /**
* Updates Nav Content.
* @param {navContent} PromoNavContent
* @returns {Observable<HttpResponse<PromoNavContent>>}
*/
  public putNavContent(navContent: PromoNavContent): Observable<HttpResponse<PromoNavItems>> {
    const uri = `${this.navItem}/${navContent.id}`;
    return this.sendRequest<PromoNavItems>('put', uri, navContent);
  }

  /**
  * removes Nav Content
  * @param {id} string
  * @returns {Observable<HttpResponse<void>>}
  */
  public removeNavContent(id: string): Observable<HttpResponse<void>> {
    const uri = `${this.navItem}/${id}`;
    return this.sendRequest<void>('delete', uri, null);
  }
  /**
    * Posts new order for Nav Items.
    * @param {any} order
    * @returns {Observable<HttpResponse<void>>}
    */
  public postNewNavItemOrder(order: Order): Observable<HttpResponse<void>> {
    return this.sendRequest<void>('post', `${this.navItem}/ordering`, order);
  }
}
