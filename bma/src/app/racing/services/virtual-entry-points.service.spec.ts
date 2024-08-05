import {  fakeAsync, tick } from '@angular/core/testing';

import { VirtualEntryPointsService } from './virtual-entry-points.service';
import { BehaviorSubject, of } from 'rxjs';

describe('VirtualEntryPointsService', () => {
  let service: VirtualEntryPointsService;
  let cmsService, windowRef;

  beforeEach(() => {
    cmsService = {
      getSportTabs: jasmine.createSpy('getSportTabs').and.returnValue(of({}))
    };
    windowRef = {
    };

    service = new VirtualEntryPointsService(cmsService, windowRef);
  });

  describe('getTabs', () => {
    it('getTabs should be created', fakeAsync(() => {
      service.sportTabs = new BehaviorSubject('') as any;
      service.getTabs('categoryId', 'display');
      tick();
    }));
  })

  describe('setTargetTab', () => {
    it('setTargetTab should be created', fakeAsync(() => {
      service.categoryId = '19'
      // service.sportTabs = new BehaviorSubject({value: [{id: 'today'}]}) as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.targetTab = new BehaviorSubject({value: [{id: 'today'}]}) as any;
      service.setTargetTab('today');
      tick();
    }));

    it('setTargetTab should be created', fakeAsync(() => {
      service.categoryId = '19'
      // service.sportTabs = new BehaviorSubject({value: [{id: 'today'}]}) as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.targetTab = new BehaviorSubject({value: [{id: 'tomorrow'}]}) as any;
      service.setTargetTab('tomorrow');
      tick();
    }));

    it('setTargetTab should be created', fakeAsync(() => {
      service.categoryId = '21'
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.targetTab = new BehaviorSubject({value: [{id: 'today'}]}) as any;
      service.setTargetTab('featured');
      tick();
    }));
  })

  describe('findBannerAccordition', () => {
    it('findBannerAccordition should be created', fakeAsync(() => {
      service['windowRef'] = {document: {querySelectorAll: () => [{innerText: 'test'}] }} as any
      service.accorditionNumber = {next: () => true} as any;
      service.lastBannerEnabled = {next: () => true} as any;
      service.targetTab = {value: {id: 'today', interstitialBanners: {bannerPosition: '0'}}} as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.findBannerAccordition();
      tick();
    }));

    it('findBannerAccordition should without value', fakeAsync(() => {
      service['windowRef'] = {document: {querySelectorAll: () => [{outerText: 'test'}] }} as any
      service.accorditionNumber = {next: () => true} as any;
      service.lastBannerEnabled = {next: () => true} as any;
      service.targetTab = {value_1: {id: 'today', interstitialBanners: {bannerPosition: '0'}}} as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.findBannerAccordition();
      tick();
    }));
    it('findBannerAccordition should without interstitialBanners', fakeAsync(() => {
      service['windowRef'] = {document: {querySelectorAll: () => [{outerText: 'test'}] }} as any
      service.accorditionNumber = {next: () => true} as any;
      service.lastBannerEnabled = {next: () => true} as any;
      service.targetTab = {value_1: {id: 'today', interstitialBanners_1: {bannerPosition: '0'}}} as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.findBannerAccordition();
      tick();
    }));

    it('findBannerAccordition should be outertext', fakeAsync(() => {
      service['windowRef'] = {document: {querySelectorAll: () => [{outerText: 'test'}] }} as any
      service.accorditionNumber = {next: () => true} as any;
      service.lastBannerEnabled = {next: () => true} as any;
      service.targetTab = {value: {id: 'today', interstitialBanners: {bannerPosition: '0'}}} as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.findBannerAccordition();
      tick();
    }));

    it('findBannerAccordition should be created', fakeAsync(() => {
      service['windowRef'] = {document: {querySelectorAll: () => [{innerText: 'test'}] }} as any
      service.accorditionNumber = {next: () => true} as any;
      service.lastBannerEnabled = {next: () => true} as any;
      service.targetTab = {value: {id: 'today', interstitialBanners: {bannerPosition: '1'}}} as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.findBannerAccordition();
      tick();
    }));

    it('findBannerAccordition should be created', fakeAsync(() => {
      service['windowRef'] = {document: {querySelectorAll: () => [{innerText: 'VIRTUAL RACING MARKET'}] }} as any
      service.accorditionNumber = {next: () => true} as any;
      service.lastBannerEnabled = {next: () => true} as any;
      service.targetTab = {value: {id: 'today', interstitialBanners: {bannerPosition: '1'}}} as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.virtualMarketName = 'virtual racing market'
      service.findBannerAccordition();
      tick();
    }));

    it('findBannerAccordition should be with out value', fakeAsync(() => {
      service['windowRef'] = {document: {querySelectorAll: () => [{innerText: 'test'}] }} as any
      service.accorditionNumber = {next: () => true} as any;
      service.lastBannerEnabled = {next: () => true} as any;
      service.targetTab = {value_1: {id: 'today', interstitialBanners: {bannerPosition: '1'}}} as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.findBannerAccordition();
      tick();
    }));

    it('findBannerAccordition should be with out intersteatial', fakeAsync(() => {
      service['windowRef'] = {document: {querySelectorAll: () => [{innerText: 'test'}] }} as any
      service.accorditionNumber = {next: () => true} as any;
      service.lastBannerEnabled = {next: () => true} as any;
      service.targetTab = {value: {id: 'today', interstitialBanners_1: {bannerPosition: '1'}}} as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.findBannerAccordition();
      tick();
    }));

    it('targetab is undefined', fakeAsync(() => {
      service['windowRef'] = {document: {querySelectorAll: () => [{innerText: 'test'}] }} as any
      service.accorditionNumber = {next: () => true} as any;
      service.lastBannerEnabled = {next: () => true} as any;
      service.sportTabs = {value: [{id: 'today'}]} as any;
      service.targetTab = undefined;
      service.findBannerAccordition();
      tick();
    }));

  })
  
})