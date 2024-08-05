import {Component, OnInit} from '@angular/core';
import { MatDialogRef } from '@angular/material/dialog';
import {ConfirmDialogComponent} from '../../shared/dialog/confirm-dialog/confirm-dialog.component';
import {BrandService} from '../../client/private/services/brand.service';
import {ExternalLink} from '../../client/private/models/externalLink.model';

@Component({
  selector: 'app-add-external-link',
  templateUrl: './add-external-link.component.html',
  styleUrls: ['./add-external-link.component.scss']
})
export class AddExternalLinkComponent implements OnInit {

  public newExternalLink: ExternalLink;

  constructor(
    private dialogRef: MatDialogRef<ConfirmDialogComponent>,
    private brandService: BrandService
  ) { }

  ngOnInit(): void {
    this.newExternalLink = {
      id: '',
      brand: this.brandService.brand,
      updatedBy: '',
      updatedAt: '',
      createdBy: '',
      createdAt: '',
      url: '',
      target: 'NEW',
      updatedByUserName: '',
      createdByUserName: ''
    };
  }

  getNewExternalLink(): ExternalLink {
    return this.newExternalLink;
  }

  isValidExternalLink(): boolean {
    return !!(this.newExternalLink.url &&
      this.newExternalLink.target);
  }

  closeDialog(): void {
    this.dialogRef.close();
  }
}
