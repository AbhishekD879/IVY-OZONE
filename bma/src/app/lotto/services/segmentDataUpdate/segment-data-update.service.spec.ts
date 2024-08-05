import { Subject } from 'rxjs';
import { SegmentDataUpdateService } from './segment-data-update.service';
import { ILottoChangeEvent } from '../../models/lotteries-config.model';

describe('SegmentDataUpdateService', () => {
  let service: SegmentDataUpdateService;

  beforeEach(() => {
    service = new SegmentDataUpdateService();
  });

  it('constructor', () => {
    expect(service).toBeTruthy();
    expect(service.dataSubject).toEqual(jasmine.any(Subject));
  });

  it('changes', () => {
    expect(service.changes).toEqual(jasmine.any(Subject));
  });
  it('changes', () => {
    service.changes = {}as ILottoChangeEvent |any
    expect(service.changes).toEqual(jasmine.any(Subject));
  });

});
