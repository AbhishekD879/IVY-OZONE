// import { Inject, Injectable, Optional } from '@angular/core';
// import { HttpClient, HttpHeaders, HttpParams, HttpResponse } from '@angular/common/http';
// import { Observable } from 'rxjs/Observable';

// import {
//   Login,
//   Token,
//   Error,
//   User,
//   Filename,
//   SvgFilename,
//   VipLevel,
//   Banner,
//   AppUpdate,
//   BetReceiptBanner,
//   BetReceiptBannerTablet,
//   BottomMenu,
//   Brand,
//   Configuration,
//   ConnectMenu,
//   Country,
//   Dashboard,
//   EdpMarket,
//   FeaturedEventsType,
//   Feature,
//   Football3DBanner,
//   FooterLogo,
//   FooterMenu,
//   Gallery,
//   HeaderMenu,
//   HomeModule,
//   HRQuickLink,
//   League,
//   LeftMenu,
//   LNQuickLink,
//   MaintenancePage,
//   ModuleRibbonTab,
//   OfferModule,
//   Offer,
//   Post,
//   Promotion,
//   QuickLink,
//   RightMenu,
//   SeoPage,
//   SportCategory,
//   Sport,
//   SsoPage,
//   StaticBlock,
//   Structure,
//   TopGame,
//   TopMenu,
//   UserMenu,
//   Widget,
//   YourCallLeague,
//   YourCallMarket,
//   YourCallStaticBlock
// } from './models';

// /**
// * Created with angular4-swagger-client-generator.
// */
// @Injectable()
// export class ApiClientService {

//   private domain = 'http://localhost/v1/api';

//   constructor(private http: HttpClient, @Optional() @Inject('domain') domain: string ) {
//     if (domain) {
//       this.domain = domain;
//     }
//   }

//   /**
//   * Allow users to log in, and to receive a JWT
//   * Method postLogin
//   * @param body username/password
//   * @return Full HTTP response as Observable
//   */
//   public postLogin(body: Login): Observable<HttpResponse<Token>> {
//     let uri = `/login`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Token>('post', uri, headers, params, JSON.stringify(body));
//   }

//   /**
//   * Method save
//   * @param Banner Banner object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Banner: Banner): Observable<HttpResponse<any>> {
//     let uri = `/banner`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Banner Banner object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Banner: Banner): Observable<HttpResponse<Banner>> {
//     let uri = `/banner`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Banner>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Banner[]>> {
//     let uri = `/banner`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Banner[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Banner>> {
//     let uri = `/banner/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Banner>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteBannerById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteBannerById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/banner/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param AppUpdate AppUpdate object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(AppUpdate: AppUpdate): Observable<HttpResponse<any>> {
//     let uri = `/app-update`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param AppUpdate AppUpdate object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(AppUpdate: AppUpdate): Observable<HttpResponse<AppUpdate>> {
//     let uri = `/app-update`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<AppUpdate>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<AppUpdate[]>> {
//     let uri = `/app-update`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<AppUpdate[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<AppUpdate>> {
//     let uri = `/app-update/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<AppUpdate>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteAppUpdateById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteAppUpdateById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/app-update/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param BetReceiptBanner BetReceiptBanner object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(BetReceiptBanner: BetReceiptBanner): Observable<HttpResponse<any>> {
//     let uri = `/bet-receipt-banner`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param BetReceiptBanner BetReceiptBanner object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(BetReceiptBanner: BetReceiptBanner): Observable<HttpResponse<BetReceiptBanner>> {
//     let uri = `/bet-receipt-banner`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<BetReceiptBanner>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<BetReceiptBanner[]>> {
//     let uri = `/bet-receipt-banner`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<BetReceiptBanner[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<BetReceiptBanner>> {
//     let uri = `/bet-receipt-banner/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<BetReceiptBanner>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteBetReceiptBannerById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteBetReceiptBannerById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/bet-receipt-banner/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param BetReceiptBannerTablet BetReceiptBannerTablet object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(BetReceiptBannerTablet: BetReceiptBannerTablet): Observable<HttpResponse<any>> {
//     let uri = `/bet-receipt-banner-tablet`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param BetReceiptBannerTablet BetReceiptBannerTablet object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(BetReceiptBannerTablet: BetReceiptBannerTablet): Observable<HttpResponse<BetReceiptBannerTablet>> {
//     let uri = `/bet-receipt-banner-tablet`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<BetReceiptBannerTablet>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<BetReceiptBannerTablet[]>> {
//     let uri = `/bet-receipt-banner-tablet`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<BetReceiptBannerTablet[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<BetReceiptBannerTablet>> {
//     let uri = `/bet-receipt-banner-tablet/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<BetReceiptBannerTablet>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteBetReceiptBannerTabletById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteBetReceiptBannerTabletById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/bet-receipt-banner-tablet/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param BottomMenu BottomMenu object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(BottomMenu: BottomMenu): Observable<HttpResponse<any>> {
//     let uri = `/bottom-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param BottomMenu BottomMenu object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(BottomMenu: BottomMenu): Observable<HttpResponse<BottomMenu>> {
//     let uri = `/bottom-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<BottomMenu>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<BottomMenu[]>> {
//     let uri = `/bottom-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<BottomMenu[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<BottomMenu>> {
//     let uri = `/bottom-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<BottomMenu>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteBottomMenuById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteBottomMenuById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/bottom-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Brand Brand object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Brand: Brand): Observable<HttpResponse<any>> {
//     let uri = `/brand`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Brand Brand object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Brand: Brand): Observable<HttpResponse<Brand>> {
//     let uri = `/brand`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Brand>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Brand[]>> {
//     let uri = `/brand`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Brand[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Brand>> {
//     let uri = `/brand/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Brand>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteBrandById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteBrandById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/brand/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Configuration Configuration object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Configuration: Configuration): Observable<HttpResponse<any>> {
//     let uri = `/configuration`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Configuration Configuration object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Configuration: Configuration): Observable<HttpResponse<Configuration>> {
//     let uri = `/configuration`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Configuration>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Configuration[]>> {
//     let uri = `/configuration`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Configuration[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Configuration>> {
//     let uri = `/configuration/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Configuration>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteConfigurationById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteConfigurationById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/configuration/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method findAllbyBrand
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findAllbyBrand(id: string): Observable<HttpResponse<Configuration>> {
//     let uri = `/configuration/brand/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Configuration>('get', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param ConnectMenu ConnectMenu object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(ConnectMenu: ConnectMenu): Observable<HttpResponse<any>> {
//     let uri = `/connect-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param ConnectMenu ConnectMenu object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(ConnectMenu: ConnectMenu): Observable<HttpResponse<ConnectMenu>> {
//     let uri = `/connect-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<ConnectMenu>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<ConnectMenu[]>> {
//     let uri = `/connect-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<ConnectMenu[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<ConnectMenu>> {
//     let uri = `/connect-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<ConnectMenu>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteConnectMenuById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteConnectMenuById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/connect-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Country Country object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Country: Country): Observable<HttpResponse<any>> {
//     let uri = `/country`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Country Country object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Country: Country): Observable<HttpResponse<Country>> {
//     let uri = `/country`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Country>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Country[]>> {
//     let uri = `/country`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Country[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Country>> {
//     let uri = `/country/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Country>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteCountryById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteCountryById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/country/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Dashboard Dashboard object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Dashboard: Dashboard): Observable<HttpResponse<any>> {
//     let uri = `/dashboard`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Dashboard Dashboard object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Dashboard: Dashboard): Observable<HttpResponse<Dashboard>> {
//     let uri = `/dashboard`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Dashboard>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Dashboard[]>> {
//     let uri = `/dashboard`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Dashboard[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Dashboard>> {
//     let uri = `/dashboard/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Dashboard>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteDashboardById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteDashboardById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/dashboard/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param EdpMarket EdpMarket object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(EdpMarket: EdpMarket): Observable<HttpResponse<any>> {
//     let uri = `/edp-market`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param EdpMarket EdpMarket object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(EdpMarket: EdpMarket): Observable<HttpResponse<EdpMarket>> {
//     let uri = `/edp-market`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<EdpMarket>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<EdpMarket[]>> {
//     let uri = `/edp-market`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<EdpMarket[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<EdpMarket>> {
//     let uri = `/edp-market/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<EdpMarket>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteEdpMarketById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteEdpMarketById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/edp-market/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param FeaturedEventsType FeaturedEventsType object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(FeaturedEventsType: FeaturedEventsType): Observable<HttpResponse<any>> {
//     let uri = `/featured-events-type`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param FeaturedEventsType FeaturedEventsType object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(FeaturedEventsType: FeaturedEventsType): Observable<HttpResponse<FeaturedEventsType>> {
//     let uri = `/featured-events-type`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<FeaturedEventsType>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<FeaturedEventsType[]>> {
//     let uri = `/featured-events-type`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<FeaturedEventsType[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<FeaturedEventsType>> {
//     let uri = `/featured-events-type/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<FeaturedEventsType>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteFeaturedEventsTypeById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteFeaturedEventsTypeById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/featured-events-type/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Feature Feature object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Feature: Feature): Observable<HttpResponse<any>> {
//     let uri = `/feature`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Feature Feature object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Feature: Feature): Observable<HttpResponse<Feature>> {
//     let uri = `/feature`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Feature>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Feature[]>> {
//     let uri = `/feature`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Feature[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Feature>> {
//     let uri = `/feature/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Feature>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteFeatureById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteFeatureById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/feature/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Football3DBanner Football3DBanner object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Football3DBanner: Football3DBanner): Observable<HttpResponse<any>> {
//     let uri = `/football-3d-banner`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Football3DBanner Football3DBanner object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Football3DBanner: Football3DBanner): Observable<HttpResponse<Football3DBanner>> {
//     let uri = `/football-3d-banner`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Football3DBanner>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Football3DBanner[]>> {
//     let uri = `/football-3d-banner`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Football3DBanner[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Football3DBanner>> {
//     let uri = `/football-3d-banner/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Football3DBanner>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteFootball3dBannerById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteFootball3dBannerById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/football-3d-banner/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param FooterLogo FooterLogo object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(FooterLogo: FooterLogo): Observable<HttpResponse<any>> {
//     let uri = `/footer-logo`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param FooterLogo FooterLogo object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(FooterLogo: FooterLogo): Observable<HttpResponse<FooterLogo>> {
//     let uri = `/footer-logo`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<FooterLogo>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<FooterLogo[]>> {
//     let uri = `/footer-logo`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<FooterLogo[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<FooterLogo>> {
//     let uri = `/footer-logo/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<FooterLogo>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteFooterLogoById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteFooterLogoById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/footer-logo/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param FooterMenu FooterMenu object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(FooterMenu: FooterMenu): Observable<HttpResponse<any>> {
//     let uri = `/footer-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param FooterMenu FooterMenu object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(FooterMenu: FooterMenu): Observable<HttpResponse<FooterMenu>> {
//     let uri = `/footer-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<FooterMenu>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<FooterMenu[]>> {
//     let uri = `/footer-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<FooterMenu[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<FooterMenu>> {
//     let uri = `/footer-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<FooterMenu>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteFooterMenuById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteFooterMenuById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/footer-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Gallery Gallery object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Gallery: Gallery): Observable<HttpResponse<any>> {
//     let uri = `/gallery`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Gallery Gallery object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Gallery: Gallery): Observable<HttpResponse<Gallery>> {
//     let uri = `/gallery`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Gallery>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Gallery[]>> {
//     let uri = `/gallery`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Gallery[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Gallery>> {
//     let uri = `/gallery/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Gallery>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteGalleryById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteGalleryById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/gallery/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param HeaderMenu HeaderMenu object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(HeaderMenu: HeaderMenu): Observable<HttpResponse<any>> {
//     let uri = `/header-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param HeaderMenu HeaderMenu object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(HeaderMenu: HeaderMenu): Observable<HttpResponse<HeaderMenu>> {
//     let uri = `/header-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<HeaderMenu>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<HeaderMenu[]>> {
//     let uri = `/header-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<HeaderMenu[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<HeaderMenu>> {
//     let uri = `/header-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<HeaderMenu>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteHeaderMenuById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteHeaderMenuById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/header-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param HomeModule HomeModule object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(HomeModule: HomeModule): Observable<HttpResponse<any>> {
//     let uri = `/home-module`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, JSON.stringify(HomeModule));
//   }

//   /**
//   * Method findAll
//   * @param active Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findAll(active: string): Observable<HttpResponse<HomeModule[]>> {
//     let uri = `/home-module`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     if (active !== undefined && active !== null) {
//       params = params.set('active', active + '');
//     }
//     return this.sendRequest<HomeModule[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<HomeModule>> {
//     let uri = `/home-module/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<HomeModule>('get', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @param HomeModule Part of HomeModule that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(id: string, HomeModule: HomeModule): Observable<HttpResponse<HomeModule>> {
//     let uri = `/home-module/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<HomeModule>('patch', uri, headers, params, JSON.stringify(HomeModule));
//   }

//   /**
//   * Method deleteHomeModuleById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteHomeModuleById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/home-module/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param HRQuickLink HRQuickLink object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(HRQuickLink: HRQuickLink): Observable<HttpResponse<any>> {
//     let uri = `/hr-quick-link`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param HRQuickLink HRQuickLink object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(HRQuickLink: HRQuickLink): Observable<HttpResponse<HRQuickLink>> {
//     let uri = `/hr-quick-link`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<HRQuickLink>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<HRQuickLink[]>> {
//     let uri = `/hr-quick-link`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<HRQuickLink[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<HRQuickLink>> {
//     let uri = `/hr-quick-link/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<HRQuickLink>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteHrQuickLinkById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteHrQuickLinkById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/hr-quick-link/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param League League object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(League: League): Observable<HttpResponse<any>> {
//     let uri = `/league`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param League League object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(League: League): Observable<HttpResponse<League>> {
//     let uri = `/league`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<League>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<League[]>> {
//     let uri = `/league`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<League[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<League>> {
//     let uri = `/league/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<League>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteLeagueById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteLeagueById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/league/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param LeftMenu LeftMenu object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(LeftMenu: LeftMenu): Observable<HttpResponse<any>> {
//     let uri = `/left-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param LeftMenu LeftMenu object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(LeftMenu: LeftMenu): Observable<HttpResponse<LeftMenu>> {
//     let uri = `/left-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<LeftMenu>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<LeftMenu[]>> {
//     let uri = `/left-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<LeftMenu[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<LeftMenu>> {
//     let uri = `/left-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<LeftMenu>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteLeftMenuById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteLeftMenuById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/left-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param LNQuickLink LNQuickLink object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(LNQuickLink: LNQuickLink): Observable<HttpResponse<any>> {
//     let uri = `/ln-quick-link`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param LNQuickLink LNQuickLink object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(LNQuickLink: LNQuickLink): Observable<HttpResponse<LNQuickLink>> {
//     let uri = `/ln-quick-link`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<LNQuickLink>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<LNQuickLink[]>> {
//     let uri = `/ln-quick-link`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<LNQuickLink[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<LNQuickLink>> {
//     let uri = `/ln-quick-link/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<LNQuickLink>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteLnQuickLinkById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteLnQuickLinkById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/ln-quick-link/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param MaintenancePage MaintenancePage object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(MaintenancePage: MaintenancePage): Observable<HttpResponse<any>> {
//     let uri = `/maintenance-page`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param MaintenancePage MaintenancePage object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(MaintenancePage: MaintenancePage): Observable<HttpResponse<MaintenancePage>> {
//     let uri = `/maintenance-page`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<MaintenancePage>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<MaintenancePage[]>> {
//     let uri = `/maintenance-page`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<MaintenancePage[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<MaintenancePage>> {
//     let uri = `/maintenance-page/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<MaintenancePage>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteMaintenancePageById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteMaintenancePageById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/maintenance-page/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param ModuleRibbonTab ModuleRibbonTab object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(ModuleRibbonTab: ModuleRibbonTab): Observable<HttpResponse<any>> {
//     let uri = `/module-ribbon-tab`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param ModuleRibbonTab ModuleRibbonTab object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(ModuleRibbonTab: ModuleRibbonTab): Observable<HttpResponse<ModuleRibbonTab>> {
//     let uri = `/module-ribbon-tab`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<ModuleRibbonTab>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<ModuleRibbonTab[]>> {
//     let uri = `/module-ribbon-tab`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<ModuleRibbonTab[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<ModuleRibbonTab>> {
//     let uri = `/module-ribbon-tab/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<ModuleRibbonTab>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteModuleRibbonTabById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteModuleRibbonTabById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/module-ribbon-tab/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param OfferModule OfferModule object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(OfferModule: OfferModule): Observable<HttpResponse<any>> {
//     let uri = `/offer-module`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param OfferModule OfferModule object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(OfferModule: OfferModule): Observable<HttpResponse<OfferModule>> {
//     let uri = `/offer-module`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<OfferModule>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<OfferModule[]>> {
//     let uri = `/offer-module`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<OfferModule[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<OfferModule>> {
//     let uri = `/offer-module/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<OfferModule>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteOfferModuleById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteOfferModuleById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/offer-module/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Offer Offer object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Offer: Offer): Observable<HttpResponse<any>> {
//     let uri = `/offer`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Offer Offer object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Offer: Offer): Observable<HttpResponse<Offer>> {
//     let uri = `/offer`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Offer>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Offer[]>> {
//     let uri = `/offer`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Offer[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Offer>> {
//     let uri = `/offer/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Offer>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteOfferById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteOfferById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/offer/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Post Post object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Post: Post): Observable<HttpResponse<any>> {
//     let uri = `/post`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Post Post object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Post: Post): Observable<HttpResponse<Post>> {
//     let uri = `/post`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Post>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Post[]>> {
//     let uri = `/post`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Post[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Post>> {
//     let uri = `/post/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Post>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deletePostById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deletePostById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/post/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Promotion Promotion object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Promotion: Promotion): Observable<HttpResponse<any>> {
//     let uri = `/promotion`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Promotion Promotion object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Promotion: Promotion): Observable<HttpResponse<Promotion>> {
//     let uri = `/promotion`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Promotion>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Promotion[]>> {
//     let uri = `/promotion`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Promotion[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Promotion>> {
//     let uri = `/promotion/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Promotion>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deletePromotionById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deletePromotionById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/promotion/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param QuickLink QuickLink object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(QuickLink: QuickLink): Observable<HttpResponse<any>> {
//     let uri = `/quick-link`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param QuickLink QuickLink object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(QuickLink: QuickLink): Observable<HttpResponse<QuickLink>> {
//     let uri = `/quick-link`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<QuickLink>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<QuickLink[]>> {
//     let uri = `/quick-link`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<QuickLink[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<QuickLink>> {
//     let uri = `/quick-link/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<QuickLink>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteQuickLinkById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteQuickLinkById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/quick-link/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param RightMenu RightMenu object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(RightMenu: RightMenu): Observable<HttpResponse<any>> {
//     let uri = `/right-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param RightMenu RightMenu object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(RightMenu: RightMenu): Observable<HttpResponse<RightMenu>> {
//     let uri = `/right-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<RightMenu>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<RightMenu[]>> {
//     let uri = `/right-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<RightMenu[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<RightMenu>> {
//     let uri = `/right-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<RightMenu>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteRightMenuById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteRightMenuById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/right-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param SeoPage SeoPage object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(SeoPage: SeoPage): Observable<HttpResponse<any>> {
//     let uri = `/seo-page`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param SeoPage SeoPage object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(SeoPage: SeoPage): Observable<HttpResponse<SeoPage>> {
//     let uri = `/seo-page`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<SeoPage>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<SeoPage[]>> {
//     let uri = `/seo-page`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<SeoPage[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<SeoPage>> {
//     let uri = `/seo-page/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<SeoPage>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteSeoPageById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteSeoPageById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/seo-page/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param SportCategory SportCategory object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(SportCategory: SportCategory): Observable<HttpResponse<any>> {
//     let uri = `/sport-category`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param SportCategory SportCategory object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(SportCategory: SportCategory): Observable<HttpResponse<SportCategory>> {
//     let uri = `/sport-category`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<SportCategory>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<SportCategory[]>> {
//     let uri = `/sport-category`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<SportCategory[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<SportCategory>> {
//     let uri = `/sport-category/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<SportCategory>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteSportCategoryById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteSportCategoryById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/sport-category/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Sport Sport object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Sport: Sport): Observable<HttpResponse<any>> {
//     let uri = `/sport`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Sport Sport object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Sport: Sport): Observable<HttpResponse<Sport>> {
//     let uri = `/sport`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Sport>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Sport[]>> {
//     let uri = `/sport`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Sport[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Sport>> {
//     let uri = `/sport/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Sport>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteSportById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteSportById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/sport/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param SsoPage SsoPage object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(SsoPage: SsoPage): Observable<HttpResponse<any>> {
//     let uri = `/sso-page`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param SsoPage SsoPage object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(SsoPage: SsoPage): Observable<HttpResponse<SsoPage>> {
//     let uri = `/sso-page`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<SsoPage>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<SsoPage[]>> {
//     let uri = `/sso-page`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<SsoPage[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<SsoPage>> {
//     let uri = `/sso-page/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<SsoPage>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteSsoPageById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteSsoPageById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/sso-page/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param StaticBlock StaticBlock object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(StaticBlock: StaticBlock): Observable<HttpResponse<any>> {
//     let uri = `/static-block`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param StaticBlock StaticBlock object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(StaticBlock: StaticBlock): Observable<HttpResponse<StaticBlock>> {
//     let uri = `/static-block`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<StaticBlock>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<StaticBlock[]>> {
//     let uri = `/static-block`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<StaticBlock[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<StaticBlock>> {
//     let uri = `/static-block/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<StaticBlock>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteStaticBlockById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteStaticBlockById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/static-block/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param Structure Structure object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Structure: Structure): Observable<HttpResponse<any>> {
//     let uri = `/structure`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Structure Structure object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Structure: Structure): Observable<HttpResponse<Structure>> {
//     let uri = `/structure`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Structure>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Structure[]>> {
//     let uri = `/structure`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Structure[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Structure>> {
//     let uri = `/structure/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Structure>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteStructureById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteStructureById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/structure/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param TopGame TopGame object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(TopGame: TopGame): Observable<HttpResponse<any>> {
//     let uri = `/top-game`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param TopGame TopGame object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(TopGame: TopGame): Observable<HttpResponse<TopGame>> {
//     let uri = `/top-game`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<TopGame>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<TopGame[]>> {
//     let uri = `/top-game`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<TopGame[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<TopGame>> {
//     let uri = `/top-game/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<TopGame>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteTopGameById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteTopGameById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/top-game/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param TopMenu TopMenu object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(TopMenu: TopMenu): Observable<HttpResponse<any>> {
//     let uri = `/top-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param TopMenu TopMenu object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(TopMenu: TopMenu): Observable<HttpResponse<TopMenu>> {
//     let uri = `/top-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<TopMenu>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<TopMenu[]>> {
//     let uri = `/top-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<TopMenu[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<TopMenu>> {
//     let uri = `/top-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<TopMenu>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteTopMenuById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteTopMenuById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/top-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param UserMenu UserMenu object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(UserMenu: UserMenu): Observable<HttpResponse<any>> {
//     let uri = `/user-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param UserMenu UserMenu object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(UserMenu: UserMenu): Observable<HttpResponse<UserMenu>> {
//     let uri = `/user-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<UserMenu>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<UserMenu[]>> {
//     let uri = `/user-menu`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<UserMenu[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<UserMenu>> {
//     let uri = `/user-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<UserMenu>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteUserMenuById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteUserMenuById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/user-menu/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param User User object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(User: User): Observable<HttpResponse<any>> {
//     let uri = `/user`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, JSON.stringify(User));
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<User[]>> {
//     let uri = `/user`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<User[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<User>> {
//     let uri = `/user/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<User>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteUserById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteUserById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/user/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @param User User object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(id: string, User: User): Observable<HttpResponse<User>> {
//     let uri = `/user/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<User>('put', uri, headers, params, JSON.stringify(User));
//   }

//   /**
//   * Method update
//   * @param User User object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(User: User): Observable<HttpResponse<User>> {
//     let uri = `/user/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<User>('patch', uri, headers, params, JSON.stringify(User));
//   }

//   /**
//   * Method save
//   * @param Widget Widget object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(Widget: Widget): Observable<HttpResponse<any>> {
//     let uri = `/widget`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param Widget Widget object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(Widget: Widget): Observable<HttpResponse<Widget>> {
//     let uri = `/widget`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Widget>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<Widget[]>> {
//     let uri = `/widget`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Widget[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<Widget>> {
//     let uri = `/widget/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<Widget>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteWidgetById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteWidgetById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/widget/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param YourCallLeague YourCallLeague object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(YourCallLeague: YourCallLeague): Observable<HttpResponse<any>> {
//     let uri = `/your-call-league`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param YourCallLeague YourCallLeague object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(YourCallLeague: YourCallLeague): Observable<HttpResponse<YourCallLeague>> {
//     let uri = `/your-call-league`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<YourCallLeague>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<YourCallLeague[]>> {
//     let uri = `/your-call-league`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<YourCallLeague[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<YourCallLeague>> {
//     let uri = `/your-call-league/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<YourCallLeague>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteYourCallLeagueById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteYourCallLeagueById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/your-call-league/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param YourCallMarket YourCallMarket object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(YourCallMarket: YourCallMarket): Observable<HttpResponse<any>> {
//     let uri = `/your-call-market`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param YourCallMarket YourCallMarket object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(YourCallMarket: YourCallMarket): Observable<HttpResponse<YourCallMarket>> {
//     let uri = `/your-call-market`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<YourCallMarket>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<YourCallMarket[]>> {
//     let uri = `/your-call-market`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<YourCallMarket[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<YourCallMarket>> {
//     let uri = `/your-call-market/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<YourCallMarket>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteYourCallMarketById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteYourCallMarketById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/your-call-market/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   /**
//   * Method save
//   * @param YourCallStaticBlock YourCallStaticBlock object that needs to be added to the storage
//   * @return Full HTTP response as Observable
//   */
//   public save(YourCallStaticBlock: YourCallStaticBlock): Observable<HttpResponse<any>> {
//     let uri = `/your-call-static-block`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('post', uri, headers, params, null);
//   }

//   /**
//   * Method update
//   * @param YourCallStaticBlock YourCallStaticBlock object that needs to be updated in the storage
//   * @return Full HTTP response as Observable
//   */
//   public update(YourCallStaticBlock: YourCallStaticBlock): Observable<HttpResponse<YourCallStaticBlock>> {
//     let uri = `/your-call-static-block`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<YourCallStaticBlock>('put', uri, headers, params, null);
//   }

//   /**
//   * Method findAll
//   * @return Full HTTP response as Observable
//   */
//   public findAll(): Observable<HttpResponse<YourCallStaticBlock[]>> {
//     let uri = `/your-call-static-block`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<YourCallStaticBlock[]>('get', uri, headers, params, null);
//   }

//   /**
//   * Method findOne
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public findOne(id: string): Observable<HttpResponse<YourCallStaticBlock>> {
//     let uri = `/your-call-static-block/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<YourCallStaticBlock>('get', uri, headers, params, null);
//   }

//   /**
//   * Method deleteYourCallStaticBlockById
//   * @param id Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.

//   * @return Full HTTP response as Observable
//   */
//   public deleteYourCallStaticBlockById(id: string): Observable<HttpResponse<any>> {
//     let uri = `/your-call-static-block/${id}`;
//     let headers = new HttpHeaders();
//     let params = new HttpParams();
//     return this.sendRequest<any>('delete', uri, headers, params, null);
//   }

//   private sendRequest<T>(method: string, uri: string, headers: HttpHeaders, params: HttpParams, body: any): Observable<HttpResponse<T>> {
//     if (method === 'get') {
//       return this.http.get<T>(this.domain + uri, { headers: headers.set('Accept', 'application/json'), params: params, observe: 'response' });
//     } else if (method === 'put') {
//       return this.http.put<T>(this.domain + uri, body, { headers: headers.set('Content-Type', 'application/json'), params: params, observe: 'response' });
//     } else if (method === 'post') {
//       return this.http.post<T>(this.domain + uri, body, { headers: headers.set('Content-Type', 'application/json'), params: params, observe: 'response' });
//     } else if (method === 'delete') {
//       return this.http.delete<T>(this.domain + uri, { headers: headers, params: params, observe: 'response' });
//     } else {
//       console.error('Unsupported request: ' + method);
//       return Observable.throw('Unsupported request: ' + method);
//     }
//   }
// }
