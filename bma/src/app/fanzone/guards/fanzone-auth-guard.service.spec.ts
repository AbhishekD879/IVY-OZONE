import { of } from 'rxjs';
import { FanzoneAuthGuard } from '@app/fanzone/guards/fanzone-auth-guard.service';
import { Router  } from '@angular/router';
import { TestBed, fakeAsync, tick } from '@angular/core/testing';
import { FanzoneStorageService } from '@app/core/services/fanzone/fanzone-storage.service';
import { CmsService } from '@app/core/services/cms/cms.service';
import { UserService } from '@app/core/services/user/user.service';

describe('FanzoneAuthGuard', () => {

  it('should call 1' , fakeAsync(()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: FanzoneStorageService,
          useValue: { get: () => {return {teamName: 'liverpool'}}},
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getFanzone: ()=> of([{teamId: 1}]) ,getMenuItems: () => of([{name: 'test',categoryId: 160, disabled: false}]), getSystemConfig: () => of({Fanzone: {enabled: true}})},
        },
        {
          provide: UserService,
          useValue: { username:'username' },
        }
      ],
    });

    const guard = TestBed.runInInjectionContext(() => FanzoneAuthGuard({} as any, {url:'/sports'} as any));
    tick();
    expect(guard).toBeTruthy();
  }))

  it('should call 2 ' , fakeAsync(()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: FanzoneStorageService,
          useValue: { get: () => {return {teamName: 'liverpool'}}},
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getFanzone: ()=> of([{teamId: 1}]) ,getMenuItems: () => of([{name: 'test',categoryId: 160, disabled: false}]), getSystemConfig: () => of({Fanzone: {enabled: false}})},
        },
        {
          provide: UserService,
          useValue: { username:'username' },
        }
      ],
    });

    const guard = TestBed.runInInjectionContext(() => FanzoneAuthGuard({} as any, {url:'/vacation'} as any));
    tick();
    expect(guard).toBeTruthy();
  }))

  it('should call 3' , fakeAsync(()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: FanzoneStorageService,
          useValue: { get: () => {return {teamName: 'liverpool'}}},
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getFanzone: ()=> of([{teamId: 1}]) ,getMenuItems: () => of([{name: 'test',categoryId: 160, disabled: false}]), getSystemConfig: () => of({Fanzone: {enabled: false}})},
        },
        {
          provide: UserService,
          useValue: { username:'username' , isUserLoggedIn: (service) => true },
        }
      ],
    });

    const guard = TestBed.runInInjectionContext(() => FanzoneAuthGuard({} as any, {url:'/vacation'} as any));
    tick();
    expect(guard).toBeTruthy();
  }))


  it('should call 3' , fakeAsync(()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: FanzoneStorageService,
          useValue: { get: () => {return {teamName: 'liverpool'}}},
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getFanzone: ()=> of([{teamId: 1}]) ,getMenuItems: () => of([{name: 'test',categoryId: 160, disabled: false}]), getSystemConfig: () => of({Fanzone: {enabled: false}})},
        },
        {
          provide: UserService,
          useValue: { username:'username' , isUserLoggedIn: (service) => true },
        }
      ],
    });

    const guard = TestBed.runInInjectionContext(() => FanzoneAuthGuard({} as any, {url:'/vacation'} as any));
    tick();
    expect(guard).toBeTruthy();
  }))

  it('should call 4' , fakeAsync(()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: FanzoneStorageService,
          useValue: { get: () => {return {teamName: 'liverpool', teamId: 1, active: true}}},
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getFanzone: ()=> of([{teamId: 1,active: true}]) ,getMenuItems: () => of([{name: '',categoryId: 160, disabled: true, fzDisabled: true}]), getSystemConfig: () => of({Fanzone: {enabled: true}})},
        },
        {
          provide: UserService,
          useValue: { username:'username' , isUserLoggedIn: (service) => true },
        }
      ],
    });

    const guard = TestBed.runInInjectionContext(() => FanzoneAuthGuard({} as any, {url:'/show-your-colours'} as any));
    tick();
    expect(guard).toBeTruthy();
  }))

  it('should call 4' , fakeAsync(()=> {
    TestBed.configureTestingModule({
      providers: [
        {
          provide: FanzoneStorageService,
          useValue: { get: () => {return {teamName: 'liverpool', teamId: 1, active: true}}},
        },
        {
          provide: Router,
          useValue: { navigate: () => true },
        },
        {
          provide: CmsService,
          useValue: { getFanzone: ()=> of([{teamId: 1,active: true}]) ,getMenuItems: () => of([{name: '',categoryId: 160, disabled: true, fzDisabled: true}]), getSystemConfig: () => of({Fanzone: {enabled: true}})},
        },
        {
          provide: UserService,
          useValue: { username:'username' , isUserLoggedIn: (service) => true },
        }
      ],
    });

    const guard = TestBed.runInInjectionContext(() => FanzoneAuthGuard({} as any, {url:'/sometext'} as any));
    tick();
    expect(guard).toBeTruthy();
  }))
    
});
