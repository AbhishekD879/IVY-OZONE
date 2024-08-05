import {Component, Input, OnInit} from '@angular/core';
import {CSVGeneratorService} from '../../client/private/services/csv.generator.service';

@Component({
  selector: 'download-cvs',
  templateUrl: './download-cvs.component.html',
  styleUrls: ['./download-cvs.component.scss'],
  providers: [
    CSVGeneratorService
  ]
})
export class DownloadCvsComponent implements OnInit {

  @Input() cvsData: any[] = [];
  @Input() cvsDataTable: any[] = []; // data with fields to create table

  /* tslint:disable */
  // Alejandro Del Rio Albrechet
  constructor(private CSVGeneratorService: CSVGeneratorService) { }
  /* tslint:enable */

  ngOnInit() {
  }

  public downloadCVS(): void {
    let isReversedProperties: string[] = [];
    const clonedCSVObject = JSON.parse(JSON.stringify(this.cvsData));
    clonedCSVObject.filter(csvRowData => {
      if (csvRowData.exclusionList){
        csvRowData.exclusionList = csvRowData.exclusionList.join(';');
      }
      if (csvRowData.inclusionList){
        csvRowData.inclusionList = csvRowData.inclusionList.join(';');
      }
    })
    this.cvsDataTable.forEach((table) => {
      if(table.hasOwnProperty('isReversed')) {
        isReversedProperties.push(table.property);
      }
    });
    isReversedProperties.forEach((prop) => {
      clonedCSVObject.forEach((obj) => obj[prop] = !obj[prop]);
    })
    this.CSVGeneratorService.downloadCSV(clonedCSVObject, this.cvsDataTable);
  }
}
