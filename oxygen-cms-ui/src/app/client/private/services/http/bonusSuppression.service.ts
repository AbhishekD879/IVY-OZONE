import { AbstractService } from "@app/client/private/services/http/transport/abstract.service";
import { Configuration } from "@app/client/private/models/configuration.model";
import { Injectable } from "@angular/core";
import { HttpClient, HttpResponse } from "@angular/common/http";
import { Observable } from "rxjs/Observable";
import { IBonusSuppressionModule, IModuleData,IAliasModuleNamesData } from "@app/bonus-suppression/models/module-manager";

@Injectable()
/**
 * module Manager service for creation removal, editing , uploading of modules
 * and prizes
 */
export class BonusSuppressionService extends AbstractService<Configuration> {
  private readonly moduleUrl: string = `rgyModule`;
  private readonly bonusSupModuleUrl: string = `rgyConfig`;
  private readonly bonusSupGlobalUrl: string = `rgy-mtaInfo`;
  private readonly aliasModuleUrl: string = `alias-module-names`;
  private moduleData: IBonusSuppressionModule[];

  /**
   * Getter for module data
   * @returns {IBonusSuppressionModule[]}
   */
  get setModuleData(): IBonusSuppressionModule[] {
    return this.moduleData;
  }

  /**
   * Setter for the module data
   * @param {IBonusSuppressionModule[]} value
   */
  set getModuleData(value: IBonusSuppressionModule[]) {
    this.moduleData = value;
  }

  constructor(http: HttpClient, domain: string, brand: string) {
    super(http, domain, brand);
  }

  /**
   * Get the list of modules created in cms for the brand
   * @returns {Observable<HttpResponse<IModuleData[]>>}
   */
  public getModules(): Observable<HttpResponse<IModuleData[]>> {
    return this.sendRequest<IModuleData[]>(
      "get",
      `${this.moduleUrl}/brand/${this.brand}`,
      null
    );
  }

  /**
   * Get the module details according to the module id
   * @param {string} moduleId
   * @returns {Observable<HttpResponse<IModuleData>>}
   */
  public getModuleById(
    moduleId: string
  ): Observable<HttpResponse<IModuleData>> {
    return this.sendRequest<IModuleData>(
      "get",
      `${this.moduleUrl}/${moduleId}`,
      null
    );
  }

  /**
   * Save the module details according to the module id
   * @param {string} moduleId
   * @param {IModuleData} formData
   * @returns {Observable<HttpResponse<IModuleData>>}
   */
  public updateModule(
    moduleId: string,
    data: any
  ): Observable<HttpResponse<IModuleData>> {
    return this.sendRequest<IModuleData>(
      "put",
      `${this.moduleUrl}/${moduleId}`,
      data
    );
  }

  /**
   * Create module for the new entry
   * @param {IModuleData} formData
   * @returns {Observable<HttpResponse<IModuleData>>}
   */
  public createModule(formData: IModuleData): Observable<HttpResponse<IModuleData>> {
    return this.sendRequest<IModuleData>("post", `${this.moduleUrl}`, formData);
  }

  /**
   * Remove module for the module id
   * @param {string} moduleId
   * @returns {Observable<HttpResponse<void>>}
   */
  public removeModuleById(moduleId: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>(
      "delete",
      `${this.moduleUrl}/${this.brand}/${moduleId}`,
      null
    );
  }

  /**
   * Get the list of modules created in cms for the brand
   * @returns {Observable<HttpResponse<IBonusSuppressionModule[]>>}
   */
   public getAllBonusSuppresionModules(): Observable<HttpResponse<IBonusSuppressionModule[]>> {
    return this.sendRequest<IBonusSuppressionModule[]>(
      "get",
      `${this.bonusSupModuleUrl}/brand/${this.brand}`,
      null
    );
  }

  /**
   * Get the module details according to the module id
   * @param {string} moduleId
   * @returns {Observable<HttpResponse<IBonusSuppressionModule>>}
   */
  public getBonusSuppresionModuleByID(
    moduleId: string
  ): Observable<HttpResponse<IBonusSuppressionModule>> {
    return this.sendRequest<IBonusSuppressionModule>(
      "get",
      `${this.bonusSupModuleUrl}/${moduleId}`,
      null
    );
  }

  /**
   * Save the module details according to the module id
   * @param {string} moduleId
   * @param {IBonusSuppressionModule} formData
   * @returns {Observable<HttpResponse<IBonusSuppressionModule>>}
   */
  public updateBonusSuppresionModuleByID(
    moduleId: string,
    formData: IBonusSuppressionModule
  ): Observable<HttpResponse<IBonusSuppressionModule>> {
    return this.sendRequest<IBonusSuppressionModule>(
      "put",
      `${this.bonusSupModuleUrl}/${moduleId}`,
      formData
    );
  }

  /**
   * Create module for the new entry
   * @param {IBonusSuppressionModule} formData
   * @returns {Observable<HttpResponse<IBonusSuppressionModule>>}
   */
  public createBonusSuppresionModule(formData: IBonusSuppressionModule): Observable<HttpResponse<IBonusSuppressionModule>> {
    return this.sendRequest<IBonusSuppressionModule>("post", `${this.bonusSupModuleUrl}`, formData);
  }

  /**
   * Remove module for the module id
   * @param {string} moduleId
   * @returns {Observable<HttpResponse<void>>}
   */
  public deleteBonusSuppresionModuleByID(moduleId: string): Observable<HttpResponse<void>> {
    return this.sendRequest<void>(
      "delete",
      `${this.bonusSupModuleUrl}/${this.brand}/${moduleId}`,
      null
    );
  }

  /**
   * to get existing global switch info
   * @returns {Observable<HttpResponse<void>>}
   */
  public getGlobalSwitch(): Observable<HttpResponse<void>> {
    return this.sendRequest<void>(
      "get",
      `${this.bonusSupGlobalUrl}/brand/${this.brand}`,
      null
    );
  }
  
  /**
   * toggle global switch data
   * @param {boolean} value
   * @returns {Observable<HttpResponse<void>>}
   */
  public toggleGlobalSwitch(value): Observable<HttpResponse<void>> {
    return this.sendRequest<void>(
      "put",
      `${this.bonusSupGlobalUrl}/${this.brand}/${value}`,
      null
    );
  }

   /**
   * Get the list of alias modules name created in cms for the brand
   * @returns {Observable<HttpResponse<IModuleDataAliasModuleNamesData[]>>}
   */
 public getAliasModulesName(): Observable<HttpResponse<IAliasModuleNamesData[]>> {
  return this.sendRequest<IAliasModuleNamesData[]>(
    "get",
    `${this.aliasModuleUrl}/brand/${this.brand}`,
    null
  );
}
}



