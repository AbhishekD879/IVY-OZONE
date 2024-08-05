import { DownloadCvsComponent } from './download-cvs.component';

describe('DownloadCvsComponent', () => {
  let component,
    CSVGeneratorService;

  beforeEach(() => {
    CSVGeneratorService = {
      downloadCSV: jasmine.createSpy('CSVGeneratorService.downloadCSV')
    };

    component = new DownloadCvsComponent(
      CSVGeneratorService
    );

    component.ngOnInit();
  });


  it('should generate CSV file for download', () => {
    component.downloadCVS();

    expect(CSVGeneratorService.downloadCSV).toHaveBeenCalled();
  });
});
