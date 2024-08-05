import { ILeg } from '../models/bet.model';
import { BuildBetDocService } from './build-bet-doc.service';

describe('BetSlipBannerService', () => {
  let service: BuildBetDocService,
    betFactoryService,
    deviceService,
    betErrorService,
    legFactoryService;

  beforeEach(() => {
    deviceService = {
      channel: {}
    };
    betErrorService = {
      push: jasmine.createSpy()
    };
    legFactoryService = {};
    betFactoryService = {};

    service = new BuildBetDocService(deviceService, betFactoryService, legFactoryService, betErrorService);
  });

  describe('@content', () => {
    const legs = [{
      winPlace: 'WIN',
      docId: 1,
      doc: jasmine.createSpy(),
      firstOutcomeId: 1
    }] as any;

    it('should return request if winPlace is WIN || SCORECAST', () => {
      const request = {
        leg: [undefined],
        legGroup: [{ legRef: [{ documentId: 1 }] }],
        returnOffers: 'N'
      } as any;
      expect(service.content(legs)).toEqual(request);
      delete legs[0].winPlace;
      legs[0].combi = 'test';
      expect(service.content(legs)).toEqual(request);
    });
  
    it('should call content() it returns picks{}', () => {
      const legs =[
        {
            isLotto:true,
            details: {
              selections : "abc",
              odds:[{}]
            },        
        },
    ]as ILeg |any
      service.content(legs)
      expect(legs[0].isLotto).toEqual(true);
      expect(legs[0].details.selections).toEqual('abc');
    });

    it('should return request if is legs.length > 1 & form leg reference of WIN legs', () => {
      legs[0].winPlace = 'WIN';
      legs[1] = {
        winPlace: 'WIN',
        docId: 2,
        doc: jasmine.createSpy(),
        firstOutcomeId: 2
      };
      expect(service.content(legs)).toEqual({
        leg: [ undefined, undefined ],
        legGroup: [
          { legRef: [{ documentId: 1 }] },
          { legRef: [{ documentId: 2 }] },
          { legRef: [{ documentId: 1 }, { documentId: 2 }] }
        ],
        returnOffers: 'N'
      } as any);
    });

    it('should form leg reference of EW legs', () => {
      legs[0].winPlace = 'EACH_WAY';
      legs[1] = {
        winPlace: 'EACH_WAY',
        docId: 2,
        doc: jasmine.createSpy(),
        firstOutcomeId: 2
      };
      expect(service.content(legs)).toEqual({
        leg: [undefined, undefined],
        legGroup: [{ legRef: [{ documentId: 1 }] }],
        returnOffers: 'N'
      } as any);
    });

    it('should check for unique outcome ids', () => {
      legs[1] = {
        winPlace: 'EACH_WAY',
        docId: 2,
        doc: jasmine.createSpy(),
        firstOutcomeId: 2
      };
      legs[2] = {
        firstOutcomeId: 3,
        doc: jasmine.createSpy()
      };
      expect(service.content(legs)).toEqual({
        leg: [undefined, undefined, undefined],
        legGroup: [{ legRef: [{ documentId: 1 }] }],
        returnOffers: 'Y'
      } as any);
    });

    it('push EW leg ref array only if all the selection in the list have EW part', () => {
      const legsWinEntity = {
        winPlace: 'WIN',
        doc: jasmine.createSpy()
      };
      const legsEWEntity = {
        winPlace: 'EACH_WAY',
        doc: jasmine.createSpy()
      };
      const legsData = [
        legsWinEntity,
        legsWinEntity,
        legsEWEntity,
        legsEWEntity
      ] as any;
      expect(service.content(legsData)).toEqual({
        leg: [undefined, undefined, undefined, undefined],
        legGroup: [{ legRef: [{ documentId: undefined }] },
          { legRef: [{ documentId: undefined }] },
          { legRef: [{ documentId: undefined}, { documentId: undefined }] },
          { legRef: [{ documentId: undefined}, { documentId: undefined }] }],
        returnOffers: 'N'
      } as any);
    });
  });
});
