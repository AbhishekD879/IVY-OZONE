import { AbstractService } from "@app/client/private/services/http/transport/abstract.service";
import { Configuration } from "@app/client/private/models/configuration.model";
import { Injectable } from "@angular/core";
import { HttpClient, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs/Observable";
import { IPrize } from "@root/app/five-a-side-showdown/models/prize-manager";
import { IContest } from "@app/five-a-side-showdown/models/contest-manager";
import { ContestManager } from "@app/client/private/models/contestManager.model";
import { Order } from "@app/client/private/models/order.model";

@Injectable()
/**
 * Contest Manager service for creation removal, editing , uploading of contests
 * and prizes
 */
export class ContestManagerService extends AbstractService<Configuration> {
  private readonly contestsUrl: string = `contest`;
  private readonly cloneContestUrl: string = `cloneContest`;
  private readonly payTableUrl: string = `contestprize`;
  private payTable: IPrize[];

  /**
   * Getter for paytable data
   * @returns {IPrize[]}
   */
  get payTableData(): IPrize[] {
    return this.payTable;
  }

  /**
   * Setter for the paytable data
   * @param {IPrize[]} value
   */
  set payTableData(value: IPrize[]) {
    this.payTable = value;
  }

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  /**
   * Get the list of contests created in cms for the brand
   * @returns {Observable<HttpResponse<IContest[]>>}
   */
  public getContests(): Observable<HttpResponse<IContest[]>> {
    return this.sendRequest<IContest[]>(
      "get",
      `${this.contestsUrl}/brand/${this.brand}`,
      null
    );
  }

  /**
   * Get the contest details according to the contest id
   * @param {string} contestId
   * @returns {Observable<HttpResponse<IContest>>}
   */
  public getContestForId(
    contestId: string
  ): Observable<HttpResponse<IContest>> {
    return this.sendRequest<IContest>(
      "get",
      `${this.contestsUrl}/${contestId}`,
      null
    );
  }

  /**
   * Save the contest details according to the contest id
   * @param {string} contestId
   * @param {IContest} formData
   * @returns {Observable<HttpResponse<IContest>>}
   */
  public saveContestChanges(
    contestId: string,
    formData: IContest
  ): Observable<HttpResponse<IContest>> {
    return this.sendRequest<IContest>(
      "put",
      `${this.contestsUrl}/${contestId}`,
      formData
    );
  }

  /**
   * Api to re order the contests in contest table
   * @param {Order} newOrder
   * @returns {Observable<HttpResponse<ContestManager[]>>}
   */
  public postNewOrder(
    newOrder: Order
  ): Observable<HttpResponse<ContestManager[]>> {
    const uri = `${this.contestsUrl}/ordering`;
    return this.sendRequest<ContestManager[]>("post", uri, newOrder);
  }

  /**
   * Upload svg images for the contest id
   * @param {string} contestId
   * @param {FormData} file
   * @returns {Observable<HttpResponse<IContest>>}
   */
  public uploadSvgImage(
    contestId: string,
    file: FormData
  ): Observable<HttpResponse<IContest>> {
    const uri = `${this.contestsUrl}/${contestId}/file`;
    return this.sendRequest<IContest>("post", uri, file);
  }

  /**
   * Create contest for the new entry
   * @param {IContest} formData
   * @returns {Observable<HttpResponse<IContest>>}
   */
  public createContest(formData: IContest): Observable<HttpResponse<IContest>> {
    return this.sendRequest<IContest>("post", `${this.contestsUrl}`, formData);
  }

  /**
   * Clone contest for the duplicate entry
   * @param {IContest} formData
   * @returns {Observable<HttpResponse<IContest>>}
   */
   public cloneContest(formData: IContest): Observable<HttpResponse<IContest>> {
    return this.sendRequest<IContest>("post", `${this.cloneContestUrl}`, formData);
  }

  /**
   * Remove contest for the contest id
   * @param {string} contestId
   * @returns {Observable<HttpResponse<void>>}
   */
  public removeContestForId(contestId: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>(
      "delete",
      `${this.contestsUrl}/${contestId}`,
      null
    );
  }

  /**
   * Get all the prizes by contest id
   * @param {string} contestId
   * @returns {Observable<HttpResponse<IPrize[]>>}
   */
  public getAllPrizesByContest(
    contestId: string
  ): Observable<HttpResponse<IPrize[]>> {
    return this.sendRequest<IPrize[]>(
      "get",
      `${this.payTableUrl}/${contestId}`,
      null
    );
  }

  /**
   * Remove the prize as per the prize id
   * @param {string} prizeId
   * @returns {Observable<HttpResponse<void>>}
   */
  public removePrize(prizeId: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>(
      "delete",
      `${this.payTableUrl}/${prizeId}`,
      null
    );
  }

  /**
   * Edit the prize by the prize id
   * @param {string} prizeId
   * @param {IPrize} prize
   * @returns {Observable<HttpResponse<IPrize>>}
   */
  public editPrizeById(
    prizeId: string,
    prize: IPrize
  ): Observable<HttpResponse<IPrize>> {
    return this.sendRequest<IPrize>(
      "put",
      `${this.payTableUrl}/${prizeId}`,
      prize
    );
  }

  /**
   * Add the prize by the prize id
   * @param {IPrize} prize
   * @returns {Observable<HttpResponse<IPrize>}
   */
  public addPrizeById(prize: IPrize): Observable<HttpResponse<IPrize>> {
    return this.sendRequest<IPrize>("post", `${this.payTableUrl}`, prize);
  }

  /**
   * Upload svg prize images
   * @param {string} prizeId
   * @param {FormData} file
   * @returns {Observable<HttpResponse<IPrize>>}
   */
  public uploadPrizeSvgImage(
    prizeId: string,
    file: FormData
  ): Observable<HttpResponse<IPrize>> {
    const uri = `${this.payTableUrl}/${prizeId}/file`;
    return this.sendRequest<IPrize>("post", uri, file);
  }
}
