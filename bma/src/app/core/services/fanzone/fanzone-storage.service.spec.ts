import { FanzoneStorageService } from './fanzone-storage.service';

describe('FanzoneStorageService', () => {
  let service: FanzoneStorageService;
  let storageService;

  beforeEach(() => {
    storageService = {
      set: jasmine.createSpy('storageService.set'),
      get: jasmine.createSpy('storageService.get').and.returnValue({ teamName: 'Everton', teamId: '123' }),
    }
    service = new FanzoneStorageService(storageService);
  });


  it('should be created', () => {
    expect(service).toBeTruthy();
  }); 

  it('encrypt and set a value to storage', ()=>{
    storageService.set = jasmine.createSpy('fanzone').and.returnValue({isNewUser: true});
    const result = service.set('fanzone', {isNewUser: true});
    expect(result).toEqual({isNewUser: true} as any);
  })

  it('encrypt and set a empty key with value to storage', ()=>{
    storageService.set = jasmine.createSpy('');
    const result = service.set('', {isNewUser: true});
    expect(result).toEqual(null);
  })

  it('encrypt and set a empty object to storage', ()=>{
    storageService.set = jasmine.createSpy('fanzone').and.returnValue({});
    const result = service.set('fanzone', {});
    expect(result).toEqual({} as any);
  })

  it('decrypt and get an empty object from storage', ()=>{
    storageService.get = jasmine.createSpy('fanzone').and.returnValue({});
    const result = service.get('fanzone');
    expect(result).toBe(null);
  })

  it('decrypt and get an empty key from storage', ()=>{
    storageService.get = jasmine.createSpy('').and.returnValue({});
    const result = service.get('');
    expect(result).toBe(null);
  })

  it('decrypt and get an object from storage', ()=>{
    storageService.get = jasmine.createSpy('fanzone').and.returnValue({isFanzoneExists: false, isResignedUser: false});
    const result = service.get('fanzone');
    expect(result).toEqual({isFanzoneExists: false, isResignedUser: false});
  })

  it('decrypt and get a encrypted string from storage', ()=>{
    storageService.get = jasmine.createSpy('fanzone').and.returnValue("eyJ0ZWFtSWQiOiI5cTBhcmJhMmtibnl3dGg4Ymt4bGhnbWRyIiwidGVhbU5hbWUiOiJDaGVsc2VhIiwic3Vic2NyaXB0aW9uRGF0ZSI6IjIwMjItMDgtMjJUMDU6MjE6NDNaIiwiaXNGYW56b25lRXhpc3RzIjp0cnVlLCJpc1Jlc2lnbmVkVXNlciI6ZmFsc2UsInRlbXBUZWFtIjp7InRlYW1JZCI6ImF2eGtuZno0ZjZvYjBydjlkYm54ZHpkZTAiLCJ0ZWFtTmFtZSI6IkxlaWNlc3RlciJ9fQ==")
    const result = service.get('fanzone');
    expect(result).toEqual({
      isFanzoneExists: true,
      isResignedUser: false,
      subscriptionDate: "2022-08-22T05:21:43Z",
      teamId: "9q0arba2kbnywth8bkxlhgmdr",
      teamName: "Chelsea",
      "tempTeam": {
        "teamId": "avxknfz4f6ob0rv9dbnxdzde0",
        "teamName": "Leicester"
      }
  });
  })
});
